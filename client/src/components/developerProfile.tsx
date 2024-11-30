import React from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, Grid } from "@mui/material";

const DeveloperProfile: React.FC = () => {
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
              onClick={() => handleNavigate("/developer_profile/age_gender")}
              fullWidth
            >
              Go to Age and Gender Analysis
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() =>
                handleNavigate("/developer_profile/education_level")
              }
              fullWidth
            >
              Go to Education Level Analysis
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() =>
                handleNavigate("/developer_profile/location_stats")
              }
              fullWidth
            >
              Go to Location Stats
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => handleNavigate("/developer_profile/coding_year")}
              fullWidth
            >
              Go to Coding Year Distribution
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() =>
                handleNavigate("/developer_profile/developer_types")
              }
              fullWidth
            >
              Go to Developer Types
            </Button>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() =>
                handleNavigate("/developer_profile/learning_resources")
              }
              fullWidth
            >
              Go to Learning Resources
            </Button>
          </Grid>
        </Grid>
      </Box>
    </>
  );
};

export default DeveloperProfile;
