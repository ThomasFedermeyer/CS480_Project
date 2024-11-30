import React from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, Grid } from "@mui/material";

const Employment: React.FC = () => {
  const navigate = useNavigate();

  const handleNavigate = (route: string) => {
    navigate(route);
  };

  return (
    <>
      <Box sx={{ p: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => handleNavigate("home")}
        >
          Home Page
        </Button>
      </Box>

      <Box sx={{ p: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => handleNavigate("/employment/companies_projects")}
              fullWidth
            >
              Go to Companies & Projects
            </Button>
          </Grid>
        </Grid>
      </Box>
    </>
  );
};

export default Employment;
