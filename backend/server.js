import express from 'express';
import cors from 'cors';
import stega from './api/stega.router.js';

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/stega", stega);
app.use('*', (req, res) => {
    res.status(404).json({error: "not found"});
})

export default app;