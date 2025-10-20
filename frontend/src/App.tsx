import React, { useCallback, useEffect, useRef, useState } from "react";

import "./App.css";
import { useImageProccess } from "./hooks/useImageProccess";
import { Status } from "./types";
import { STATUS } from "./utils/constants";

type ImageState = {
  original: string | null;
  processed: string | null;
};

const App: React.FC = () => {
  const [images, setImages] = useState<ImageState>({
    original: null,
    processed: null,
  });
  const { processImage } = useImageProccess();
  const [algorithm, setAlgorithm] = useState<string>("");
  const [kernelSize, setKernelSize] = useState<number>(3);
  const [file, setFile] = useState<File>();
  const inputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState<Status>(STATUS.IDLE);

  const handleProccessImage = useCallback(
    async (file: File, algorithm: string, kernelSize: number) => {
      setStatus(STATUS.LOADING);
      const formData = new FormData();
      formData.append("image", file);
      formData.append("algorithm", algorithm);
      formData.append("kernel_size", kernelSize.toString());

      try {
        const response = await processImage(formData);

        if (response.isOk && response.data) {
          setImages((prev) => ({
            ...prev,
            processed: `data:image/jpeg;base64,${response.data}`,
          }));
          setStatus(STATUS.SUCCESS);
        } else {
          console.error("Error processing image:", response.error);
          setStatus(STATUS.ERROR);
        }
      } catch (error) {
        setStatus(STATUS.ERROR);
      }
    },
    []
  );

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const originalUrl = URL.createObjectURL(file);
    setImages({ original: originalUrl, processed: null });
    setFile(file);
  };

  const handleChangeAlgorithm = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setAlgorithm(e.target.value);
  };

  const handleChangeKernelSize = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newKernelSize = parseInt(e.target.value);
    setKernelSize(newKernelSize);
  };

  const handleDownload = () => {
    if (!images.processed) return;

    // Tạo tên file thông minh
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, "-");
    const algorithmName = algorithm.replace("_", "-");
    const kernelInfo =
      algorithm === "median" ? `_kernel${kernelSize}x${kernelSize}` : "";
    const filename = `processed_${algorithmName}${kernelInfo}_${timestamp}.jpg`;

    const link = document.createElement("a");
    link.href = images.processed;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleReset = () => {
    setImages({ original: null, processed: null });
    setAlgorithm("");
    setKernelSize(3);
    setStatus(STATUS.IDLE);
    setFile(undefined);
    if (!inputRef.current) return;
    inputRef.current.value = "";
  };

  useEffect(() => {
    if (!file || !algorithm) return;
    handleProccessImage(file, algorithm, kernelSize);
  }, [file, algorithm, kernelSize]);

  return (
    <>
      <h1>Ứng dụng Xử lý ảnh</h1>
      <div
        style={{
          display: "flex",
          gap: "16px",
          alignItems: "center",
        }}
      >
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          ref={inputRef}
          disabled={status === STATUS.LOADING}
        />
        <select
          value={algorithm}
          onChange={handleChangeAlgorithm}
          disabled={status === STATUS.LOADING}
        >
          <option value="">Chọn thuật toán</option>
          <option value="median">Lọc trung vị (Median Filter)</option>
          <option value="canny">Phát hiện biên (Canny)</option>
        </select>
        <select
          value={kernelSize}
          onChange={handleChangeKernelSize}
          disabled={status === STATUS.LOADING}
        >
          <option value={3}>Kernel 3x3</option>
          <option value={5}>Kernel 5x5</option>
          <option value={7}>Kernel 7x7</option>
          <option value={9}>Kernel 9x9</option>
        </select>
        <button
          onClick={handleDownload}
          disabled={status === STATUS.LOADING || !images.processed}
          className="download-btn"
        >
          Lưu kết quả
        </button>
        <button onClick={handleReset} disabled={status === STATUS.LOADING}>
          Reset
        </button>
      </div>

      {/* Status indicator */}
      <div className="status-message">
        {status === STATUS.LOADING && (
          <>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "10px",
              }}
            >
              <div className="spinner"></div>
              <span>Đang xử lý ảnh...</span>
            </div>
            <div className="progress-bar">
              <div className="progress-bar-fill"></div>
            </div>
          </>
        )}

        {status === STATUS.ERROR && (
          <span className="status-error">
            ❌ Lỗi xử lý ảnh. Vui lòng thử lại.
          </span>
        )}

        {status === STATUS.SUCCESS && (
          <span className="status-success">
            ✅ Xử lý ảnh thành công!
            {algorithm === "median" && ` (Kernel ${kernelSize}x${kernelSize})`}
            {algorithm === "median_opt" &&
              ` (Kernel ${kernelSize}x${kernelSize} - Tối ưu)`}
          </span>
        )}
      </div>

      <div className="image-container-wrapper">
        <div className="image-container">
          <h2>Before</h2>
          {images.original ? (
            <img src={images.original} alt="Gốc" />
          ) : (
            <div className="placeholder">
              <p>Chưa có ảnh gốc</p>
            </div>
          )}
        </div>

        <div className="image-container">
          <h2>After</h2>
          {images.processed ? (
            <img src={images.processed} alt="Xử lý" />
          ) : (
            <div className="placeholder">
              <p>Chưa có ảnh xử lý</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default App;
