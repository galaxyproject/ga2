// import type { NextApiRequest, NextApiResponse } from "next";

// export default async function handler(req: NextApiRequest, res: NextApiResponse) {
//   const { url } = req.query;
//   console.log('GETTING DATA ', url)
//   if (!url || typeof url !== "string") {
//     return res.status(400).json({ error: "URL is required" });
//   }

//   try {
//     const response = await fetch(url);
//     const buffer = Buffer.from(await response.arrayBuffer());
//     const contentType = 'application/gzip'  // response.headers.get("Content-Type") || "application/octet-stream";

//     // res.setHeader("Access-Control-Allow-Origin", "*");
//     res.setHeader("Content-Type", contentType);
//     // console.log('GETTING DATA ', contentType) 
//     res.setHeader("Content-Encoding", "gzip");
//     res.send(buffer);
//   } catch (error) {
//     res.status(500).json({ error: "Internal Server Error" });
//   }
// }


import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";
import { promisify } from "util";
import zlib from "zlib";
import { v4 as uuidv4 } from "uuid";

const pipeline = promisify(require("stream").pipeline);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { url } = req.query;

  if (!url || typeof url !== "string") {
    return res.status(400).json({ error: "URL is required" });
  }

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.statusText}`);
    }

    const tempFolder = path.join(process.cwd(), "tmp");
    if (!fs.existsSync(tempFolder)) fs.mkdirSync(tempFolder);

    const gzPath = path.join(tempFolder, `${uuidv4()}.png.gz`);
    const imgPath = gzPath.replace(".gz", "");

    // Download and decompress the file
    await pipeline(response.body, fs.createWriteStream(gzPath));
    await pipeline(fs.createReadStream(gzPath), zlib.createGunzip(), fs.createWriteStream(imgPath));

    // ✅ Stream the file manually instead of using res.sendFile
    res.setHeader("Content-Type", "image/png");

    const stream = fs.createReadStream(imgPath);
    stream.pipe(res);

    // Cleanup after the stream ends
    stream.on("close", () => {
      fs.unlink(gzPath, () => {});
      fs.unlink(imgPath, () => {});
    });

    stream.on("error", (err) => {
      console.error("Stream error:", err);
      res.status(500).json({ error: "Error streaming the image." });
    });
  } catch (error) {
    console.error("Server Error:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
}
