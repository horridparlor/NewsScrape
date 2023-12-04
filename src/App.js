import React, { useState } from 'react';
import {
    TextField,
    Button,
    Box,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    FormGroup,
    FormControlLabel,
    Switch,
    CircularProgress
} from '@mui/material';

function App() {
    const [name, setName] = useState('');
    const [age, setAge] = useState('');
    const [language, setLanguage] = useState('');
    const [location, setLocation] = useState('');
    const [loading, setLoading] = useState(false);
    const [genres, setGenres] = useState({
        sports: false,
        culture: false,
        music: false,
    });
    const [response, setResponse] = useState('');

    const handleGenreChange = (event) => {
        setGenres({ ...genres, [event.target.name]: event.target.checked });
    };

    const handleSubmit = async () => {
        setLoading(true);
        const requestData = {
            name,
            age,
            language,
            location,
            genres,
        };

        const response = await fetch('http://localhost:5000/greet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        });

        const data = await response.json();
        setLoading(false);
        setResponse(data.message);
    };

    function messageToDivs(message) {
        if (message === undefined) {
            return <div>Response</div>;
        }
        const lines = message.split('\n');

        return (
            <div>
                {lines.map((line, index) => (
                    <>
                        <br/>
                        <div key={index}>{line}</div>
                    </>
                ))}
            </div>
        );
    }

    return (
        <Box sx={{ m: 2 }}>
            <TextField
                label="Name"
                variant="outlined"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <TextField
                label="Age"
                variant="outlined"
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
            />

            <FormControl fullWidth margin="normal">
                <InputLabel>Language</InputLabel>
                <Select
                    value={language}
                    label="Language"
                    onChange={(e) => setLanguage(e.target.value)}
                >
                    <MenuItem value="English">English</MenuItem>
                    <MenuItem value="Finnish">Finnish</MenuItem>
                </Select>
            </FormControl>

            <FormControl fullWidth margin="normal">
                <InputLabel>Location</InputLabel>
                <Select
                    value={location}
                    label="Location"
                    onChange={(e) => setLocation(e.target.value)}
                >
                    <MenuItem value="Pori">Pori</MenuItem>
                    <MenuItem value="Rauma">Rauma</MenuItem>
                    <MenuItem value="Ulvila">Ulvila</MenuItem>
                    <MenuItem value="Eurajoki">Eurajoki</MenuItem>
                    <MenuItem value="Eura">Eura</MenuItem>
                    <MenuItem value="Nakkila">Nakkila</MenuItem>
                    <MenuItem value="Pomarkku">Pomarkku</MenuItem>
                    <MenuItem value="Harjavalta">Harjavalta</MenuItem>
                    <MenuItem value="Kokemäki">Kokemäki</MenuItem>
                    <MenuItem value="Huittinen">Huittinen</MenuItem>
                    <MenuItem value="Jämijärvi">Jämijärvi</MenuItem>
                    <MenuItem value="Kankaanpää">Kankaanpää</MenuItem>
                    <MenuItem value="Siikainen">Siikainen</MenuItem>
                    <MenuItem value="Merikarvia">Merikarvia</MenuItem>
                    <MenuItem value="Karvia">Karvia</MenuItem>

                </Select>
            </FormControl>

            <FormGroup>
                {Object.entries(genres).map(([genre, value]) => (
                    <FormControlLabel
                        control={<Switch checked={value} onChange={handleGenreChange} name={genre} />}
                        label={genre.charAt(0).toUpperCase() + genre.slice(1)}
                        key={genre}
                    />
                ))}
            </FormGroup>

            <Button variant="contained" onClick={handleSubmit}>
                Send
            </Button>
            {loading && (
                <Box sx={{ display: 'flex', justifyContent: 'center', m: 2 }}>
                    <CircularProgress />
                </Box>
            )}
            <Box>
                {messageToDivs(response)}
            </Box>
        </Box>
    );
}

export default App;
