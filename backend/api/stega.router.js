import express from 'express';
import EncodeController from './encode.controller.js';
import DecodeController from './decode.controller.js';

const router = express.Router();

router.route("/encode").post(EncodeController.apiUploadImg);
router.route("/decoed").post(DecodeController.apiUploadImg);