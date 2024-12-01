import React from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, Grid } from "@mui/material";

const PopularTechnologies: React.FC = () => {
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
              onClick={() =>
                handleNavigate("/popular_technologies/technologies")
              }
              fullWidth
            >
              Go to Technologies
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => handleNavigate("/popular_technologies/tools")}
              fullWidth
            >
              Go to Tools
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() =>
                handleNavigate("/popular_technologies/resources_per_technology")
              }
              fullWidth
            >
              Go to Resources Per Technology
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() =>
                handleNavigate("/popular_technologies/resources_per_tool")
              }
              fullWidth
            >
              Go to Resources Per Tool
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() =>
                handleNavigate(
                  "/popular_technologies/user_and_developer_per_technology"
                )
              }
              fullWidth
            >
              Go to User and Developer Per Technology
            </Button>
          </Grid>
        </Grid>
      </Box>
    </>
  );
};

export default PopularTechnologies;
