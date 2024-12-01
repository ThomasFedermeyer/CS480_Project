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
import GetEmploymentStatus from "./components/employment/getEmploymentStatus";
import AverageSalary from "./components/employment/averageSalary";
import PopularTechnologies from "./components/popular_technologies";
import Technologies from "./components/popular_technologies/technologies";
import Tools from "./components/popular_technologies/tools";
import ResourcesPerTechnology from "./components/popular_technologies/resourcesPerTechnology";
import ResourcesPerTool from "./components/popular_technologies/resourcesPerTool";
import UserAndDeveloperPerTechnology from "./components/popular_technologies/userAndDeveloperPerTechnology";

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
          <Route
            path="/employment/employment_status"
            element={<GetEmploymentStatus />}
          />
          <Route
            path="/employment/average_salary"
            element={<AverageSalary />}
          />
          <Route
            path="/popular_technologies"
            element={<PopularTechnologies />}
          />
          <Route
            path="/popular_technologies/technologies"
            element={<Technologies />}
          />
          <Route
            path="/popular_technologies/technologies"
            element={<Technologies />}
          />
          <Route path="/popular_technologies/tools" element={<Tools />} />
          <Route
            path="/popular_technologies/resources_per_technology"
            element={<ResourcesPerTechnology />}
          />
          <Route
            path="/popular_technologies/resources_per_tool"
            element={<ResourcesPerTool />}
          />
          <Route
            path="/popular_technologies/user_and_developer_per_technology"
            element={<UserAndDeveloperPerTechnology />}
          />
          <Route path="*" element={<Navigate to="/home" />} />
        </Routes>
      </Box>
    </BrowserRouter>
  );
}

export default App;
