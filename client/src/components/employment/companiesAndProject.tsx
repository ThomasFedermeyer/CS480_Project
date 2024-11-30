import React from "react";
import { Box, Typography } from "@mui/material";

const CompaniesAndProject: React.FC = () => {
  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        Companies and Projects
      </Typography>
      <Typography variant="body1">
        This is a sample component for displaying information about companies
        and projects.
      </Typography>
    </Box>
  );
};

export default CompaniesAndProject;
