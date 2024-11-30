import React from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button } from "@mui/material";

const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleNavigate = (route: string) => {
    navigate(route);
  };

  return (
    <Box sx={{ p: 2 }}>
      <h1>Home Page</h1>
      <p>Welcome to the Home page.</p>
      <Button
        variant="contained"
        color="primary"
        onClick={() => handleNavigate("/developer_profile")}
        sx={{ mr: 2 }}
      >
        Go to Developer Profile
      </Button>
      <Button
        variant="contained"
        color="primary"
        onClick={() => handleNavigate("/employment")}
      >
        Go to Employment
      </Button>
    </Box>
  );
};

export default Home;
