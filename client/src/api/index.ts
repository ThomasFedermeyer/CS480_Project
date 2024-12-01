import {
  AgeGenderByLevelAPIResponse,
  APIAvgYearsCodingByDeveloperTypeResponse,
  APIAvgYearsCodingByLocationResponse,
  APICompaniesResponse,
  APIEducationLevelAPIResponse,
  APILearningResourcesResponse,
  APIRemotePolicyResponse,
  APITechCountResponse,
  APITechnologiesResponse,
  APITechResourcesResponse,
  APITechSalaryResponse,
  APIToolResourcesResponse,
  APIToolsResponse,
  APIYearsCodingGroupResponse,
  CodingLevelType,
  DemographicsType,
} from "./interfaces";

const baseURL = "http://localhost:8000";

export const getAgeAndGenderByLevel = async (
  demographic: DemographicsType,
  codingLevelFilter: CodingLevelType
): Promise<AgeGenderByLevelAPIResponse> => {
  try {
    let params = "";
    if (demographic) {
      params = params + "demographic=" + demographic;
    }
    if (codingLevelFilter)
      params =
        params +
        `${demographic ? "&codingLevelFilter=" : "codingLevelFilter="}` +
        codingLevelFilter;

    if (params.length > 0) {
      params = "?" + params;
    }
    const response = await fetch(
      `${baseURL}/api/developer_profile/ageAndGenderByLevel${params.toString()}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: AgeGenderByLevelAPIResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const getEducationLevel =
  async (): Promise<APIEducationLevelAPIResponse> => {
    try {
      const response = await fetch(
        `${baseURL}/api/developer_profile/educationLevel`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: APIEducationLevelAPIResponse = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };

export const getLocationStats =
  async (): Promise<APIAvgYearsCodingByLocationResponse> => {
    try {
      const response = await fetch(
        `${baseURL}/api/developer_profile/locationStats`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: APIAvgYearsCodingByLocationResponse = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };

export const getYearsCodingDistribution =
  async (): Promise<APIYearsCodingGroupResponse> => {
    try {
      const response = await fetch(
        `${baseURL}/api/developer_profile/yearsCodingDistribution`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: APIYearsCodingGroupResponse = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };

export const getDeveloperTypesAndYearsCoding =
  async (): Promise<APIAvgYearsCodingByDeveloperTypeResponse> => {
    try {
      const response = await fetch(
        `${baseURL}/api/developer_profile/developerTypesAndYearsCoding`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: APIAvgYearsCodingByDeveloperTypeResponse =
        await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };

export const getLearningResources = async (
  byLearning: boolean | null,
  byAge: boolean | null
): Promise<APILearningResourcesResponse> => {
  try {
    let params = "";
    if (byLearning) {
      params = params + "byLearning=" + byLearning;
    }
    if (byAge) {
      params = params + `${byLearning ? "&byAge=" : "byAge="}` + byAge;
    }

    if (params.length > 0) {
      params = "?" + params;
    }
    const response = await fetch(
      `${baseURL}/api/developer_profile/learningResources${params.toString()}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: APILearningResourcesResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const getCompaniesAndProjects = async (
  page: number,
  filter: string,
  filterValue: string
): Promise<APICompaniesResponse> => {
  try {
    let params = `page=${page}`;
    if (filter && filterValue) {
      params += `&${filter}=${filterValue}`;
    }

    const response = await fetch(
      `${baseURL}/api/employment/getCompaniesAndProjects?${params}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: APICompaniesResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const getRemotePolicyByLocation = async (
  distributionOf: string | null,
  byLocation: boolean | null
): Promise<APIRemotePolicyResponse> => {
  try {
    let params = "";
    if (distributionOf) {
      params += `distributionOf=${distributionOf}`;
    }
    if (byLocation) {
      params += `${params ? "&" : ""}byLocation=${byLocation}`;
    }

    const response = await fetch(
      `${baseURL}/api/employment/getEmploymentStatus${
        params ? "?" + params : ""
      }`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: APIRemotePolicyResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const getAverageSalary = async (
  groupBy: "DeveloperTypeName" | "TechName" | null
): Promise<APITechSalaryResponse> => {
  try {
    let params = "";
    if (groupBy) {
      params += `groupBy=${groupBy}`;
    }

    const response = await fetch(
      `${baseURL}/api/employment/averageSalary${params ? "?" + params : ""}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: APITechSalaryResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const getTechnologies = async (
  page: number,
  filter: string | null,
  filterValue: string | null,
  sortOrder: string | null,
  sortType: string | null
): Promise<APITechnologiesResponse> => {
  try {
    let params = `page=${page}`;
    if (filter && filterValue) {
      params += `&${filter}=${filterValue}`;
    }
    if (sortOrder) {
      params += `&sort=${sortOrder}`;
    }
    if (sortType) {
      params += `&sortBy=${sortType}`;
    }

    const response = await fetch(
      `${baseURL}/api/popular_technologies/getTechnologies?${params}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: APITechnologiesResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const getTools = async (
  page: number,
  filter: string | null,
  filterValue: string | null,
  sortOrder: string | null,
  sortType: string | null
): Promise<APIToolsResponse> => {
  try {
    let params = `page=${page}`;
    if (filter && filterValue) {
      params += `&${filter}=${filterValue}`;
    }
    if (sortOrder) {
      params += `&sort=${sortOrder}`;
    }
    if (sortType) {
      params += `&sortBy=${sortType}`;
    }

    const response = await fetch(
      `${baseURL}/api/popular_technologies/getTools?${params}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: APIToolsResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

export const getResourcesPerTechnology =
  async (): Promise<APITechResourcesResponse> => {
    try {
      const response = await fetch(
        `${baseURL}/api/popular_technologies/getResourcesPerTechnology`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: APITechResourcesResponse = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };

export const getResourcesPerTool =
  async (): Promise<APIToolResourcesResponse> => {
    try {
      const response = await fetch(
        `${baseURL}/api/popular_technologies/getResourcesPerTool`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: APIToolResourcesResponse = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };

export const getUsersAndDeveloperTypesPerTechnology = async (
  developerTypeName: string | null
): Promise<APITechCountResponse> => {
  try {
    let params = "";
    if (developerTypeName) {
      params += `developerTypeName=${developerTypeName}`;
    }

    const response = await fetch(
      `${baseURL}/api/popular_technologies/getUsersAndDeveloperTypesPerTechnology${
        params ? "?" + params : ""
      }`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: APITechCountResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};
