import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Box } from "@mui/material";
import GenderAgeLevel from "./components/developer_profile/genderAgeLevel";
import EducationLevel from "./components/developer_profile/educationLevel";
import LocationStats from "./components/developer_profile/locationStats";
import CodingYear from "./components/developer_profile/codingYear";
import DeveloperTypes from "./components/developer_profile/developerTypes";
import LearningResources from "./components/developer_profile/learningResources";
import Employment from "./components/employment";
import CompaniesAndProject from "./components/employment/companiesAndProject";
import DeveloperProfile from "./components/developerProfile";
import Home from "./components/home";

function App() {
  return (
    <BrowserRouter>
      <Box sx={{ mt: 8 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<Home />} />
          <Route path="/developer_profile" element={<DeveloperProfile />} />
          <Route
            path="/developer_profile/age_gender"
            element={<GenderAgeLevel />}
          />
          <Route
            path="/developer_profile/education_level"
            element={<EducationLevel />}
          />
          <Route
            path="/developer_profile/location_stats"
            element={<LocationStats />}
          />
          <Route
            path="/developer_profile/coding_year"
            element={<CodingYear />}
          />
          <Route
            path="/developer_profile/developer_types"
            element={<DeveloperTypes />}
          />
          <Route
            path="/developer_profile/developer_types"
            element={<DeveloperTypes />}
          />
          <Route
            path="/developer_profile/learning_resources"
            element={<LearningResources />}
          />

          <Route path="/employment" element={<Employment />} />
          <Route
            path="/employment/companies_projects"
            element={<CompaniesAndProject />}
          />
          <Route path="*" element={<Navigate to="/home" />} />
        </Routes>
      </Box>
    </BrowserRouter>
  );
}

export default App;
