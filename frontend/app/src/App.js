import './App.css';
import React from 'react';
import {Form, Button, Container} from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
import {useState} from "react";
import "react-image-crop/dist/ReactCrop.css";
import ReactCrop from "react-image-crop";


function App() {

    const [srcImg, setSrcImg] = useState(null);
    const [image, setImage] = useState(null);
    const [crop, setCrop] = useState({aspect: 16 / 9});
    const [result, setResult] = useState(null);

    const handleImage = async (event) => {
        setSrcImg(URL.createObjectURL(event.target.files[0]));
        console.log(event.target.files[0]);
    };
    //以下のconstがトリミング機能　ここに俺の作ったやつが実行出来るコードを描けばいい
    //絶対ここだわ　ここに実行コード書けば解決するわ　ここ！！！！めっちゃここ！！！
    const getCroppedImg = async () => {
        try {
            const canvas = document.createElement("canvas");
            const scaleX = image.naturalWidth / image.width;
            const scaleY = image.naturalHeight / image.height;
            canvas.width = crop.width;
            canvas.height = crop.height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(
                image,
                crop.x * scaleX,
                crop.y * scaleY,
                crop.width * scaleX,
                crop.height * scaleY,
                0,
                0,
                crop.width,
                crop.height
            );
            //これが画像データ？
            const base64Image = canvas.toDataURL("image/jpeg", 1);
            setResult(base64Image);
            console.log(result);
        } catch (e) {
            console.log("crop the image");
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log(result);
    }

    return (
        <Container className="container" fluid="md">
            <h5 className="header">React Image Crop</h5>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Select Image you want to crop</Form.Label>
                    <div>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImage}
                        />
                    </div>
                    <div>
                        {srcImg && (
                            <div>
                                <ReactCrop
                                    style={{maxWidth: "50%"}}
                                    src={srcImg}
                                    onImageLoaded={setImage}
                                    crop={crop}
                                    onChange={setCrop}
                                />
                                <Button className="cropButton" onClick={getCroppedImg}>
                                    crop
                                </Button>
                            </div>
                        )}
                        {result && (
                            <div>
                                <img src={result} alt="cropped image"/>
                            </div>
                        )}
                    </div>
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </Container>
    );
}

export default App;

/*
  課題
  １．ここで読み込んだ画像データをFlaskに送る必要があるね
  ２．Flaskからもう一度ここに送らなければならない(修正後のデータ)⇐多分これは送信に成功すればすぐ
  ３．画像の並列化とpdf化を進めなければならないね
*/