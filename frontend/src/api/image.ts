import axios from "axios";
import { BASE_URL } from "../utils/constants";

export type APIResponseSuccess = {
  data: {
    processed_image: string;
  };
};

export type APIResponseError = {
  error: string;
};

export type APIResponse = APIResponseSuccess | APIResponseError;

export const imageProccesing = (formData: FormData) => {
  return axios
    .post(`${BASE_URL}/process`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((response) => {
      console.log("Axios response:", response);
      console.log("Response data:", response.data);
      return response;
    });
};
