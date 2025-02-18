import { Fragment } from "react";

interface FormattedValueCellProps {
  value: number;
}

function formatLargeNumber(value: number): string {
  if (value >= 1e9) return `${(value / 1e9).toFixed(1)}G`;
  if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`;
  if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
  return value.toString();
}

export const FormattedNumber = ({
  value,
}: FormattedValueCellProps): JSX.Element => {
  return <Fragment>{formatLargeNumber(value)}</Fragment>;
};
