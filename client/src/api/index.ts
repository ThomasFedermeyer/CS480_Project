import {
  AgeGenderByLevelAPIResponse,
  APIAvgYearsCodingByDeveloperTypeResponse,
  APIAvgYearsCodingByLocationResponse,
  APIEducationLevelAPIResponse,
  APILearningResourcesResponse,
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
