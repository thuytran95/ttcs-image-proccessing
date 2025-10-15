import React from "react";
import { imageProccesing, APIResponse } from "../api/image";

type HookResponse = {
  data: string | null;
  isOk: boolean;
  error?: string;
};

export const useImageProccess = () => {
  const processImage = async (formData: FormData): Promise<HookResponse> => {
    try {
      const response = await imageProccesing(formData);
      console.log("API Response:", response.data);

      if (response.data.processed_image) {
        return {
          data: response.data.processed_image,
          isOk: true,
        };
      } else {
        return {
          data: null,
          isOk: false,
          error: response.data.error || "No processed image received",
        };
      }
    } catch (error) {
      console.error("API Error:", error);
      if (error instanceof Error) {
        return { data: null, isOk: false, error: error.message };
      }
      return { data: null, error: "Unknown", isOk: false };
    }
  };

  return { processImage };
};
