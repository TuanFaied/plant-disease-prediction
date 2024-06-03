import React, { useState } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { message, Upload } from 'antd';
import axios from 'axios';

const { Dragger } = Upload;

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [filePreview, setFilePreview] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const draggerProps = {
        name: 'file',
        multiple: false,
        beforeUpload: (file) => {
            setFile(file);
            setFilePreview(URL.createObjectURL(file));
            return false; // Prevent the default upload behavior
        },
        onChange(info) {
            const { status } = info.file;
            if (status !== 'uploading') {
                console.log(info.file, info.fileList);
            }
            if (status === 'done') {
                message.success(`${info.file.name} file uploaded successfully.`);
            } else if (status === 'error') {
                message.error(`${info.file.name} file upload failed.`);
            }
        },
        onRemove: () => {
            setFile(null);
            setFilePreview(null);
        },
        onDrop(e) {
            console.log('Dropped files', e.dataTransfer.files);
        },
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError("Please upload a file first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            setLoading(true);
            setError(null);
            const response = await axios.post('http://127.0.0.1:5000/predict', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setPrediction(response.data.predicted_class);
        } catch (err) {
            setError("An error occurred while making the prediction.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Plant Disease Prediction</h1>
            <Dragger {...draggerProps}>
                <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p className="ant-upload-text">Click or drag file to this area to upload</p>
                <p className="ant-upload-hint">
                    Support for a single or bulk upload. Strictly prohibited from uploading company data or other
                    banned files.
                </p>
            </Dragger>
            {filePreview && (
                <div style={{ marginTop: 20 }}>
                    <img src={filePreview} alt="preview" style={{ maxWidth: '100%', maxHeight: 400 }} />
                </div>
            )}
            <form onSubmit={handleSubmit}>
                <button type="submit">Upload and Predict</button>
            </form>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {prediction !== null && <p>Predicted Class: {prediction}</p>}
        </div>
    );
};

export default FileUpload;
