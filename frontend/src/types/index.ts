import { STATUS } from "../utils/constants";

export type Status = (typeof STATUS)[keyof typeof STATUS];
