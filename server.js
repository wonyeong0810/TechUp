const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());

app.get('/recommendation', async (req, res) => {
    const difficulty = req.query.difficulty;

    if (difficulty < 1 || difficulty > 30) {
        return res.status(400).json({ error: 'Invalid difficulty specified' });
    }

    try {
        const response = await axios.get('https://solved.ac/api/v3/search/problem', {
            params: {
                query: `tier:${difficulty}`,
                sort: 'random',
                page: 1,
                size: 1
            }
        });

        if (response.data.count > 0) {
            const problem = response.data.items[0];
            res.json({
                problem: {
                    id: problem.problemId,
                    title: problem.titleKo,
                    tier: problem.level
                }
            });
        } else {
            res.status(404).json({ error: 'No problems found for the specified difficulty' });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Problem recommendation error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
