export interface CommonAPIResponse {
  error: false;
  message: string;
}

export type AgeGroupType =
  | "0-18"
  | "19-25"
  | "26-35"
  | "36-45"
  | "46-55"
  | "56-65"
  | "66-100";

export type GenderType = "M" | "F" | "O";

export type GenericCount = { counts: number };

export type APIGenderAPIResponseTypes<T extends "Gender" | "AgeGroup"> = {
  data: Array<
    {
      [key in T]: T extends "Gender" ? GenderType : AgeGroupType;
    } & GenericCount
  >;
};

export type DemographicsType = "Gender" | "Age" | null;
export type CodingLevelType = "Learning" | "Professional" | null;

export interface APIGenderAPIRequest {
  demographics: DemographicsType;
  codingLevel: CodingLevelType;
}

export type GenericAPIResponse<T> = T & CommonAPIResponse;

export type AgeGenderByLevelAPIResponse =
  | GenericAPIResponse<APIGenderAPIResponseTypes<"Gender">>
  | GenericAPIResponse<APIGenderAPIResponseTypes<"AgeGroup">>;

export type EducationLevelType =
  | "Primary/elementary school"
  | "Secondary school"
  | "Bachelor's degree"
  | "Master's degree"
  | "Professional degree"
  | "Something else";

export type EducationLevelCount = {
  EducationLevel: EducationLevelType;
} & GenericCount;

export type APIEducationLevelAPIResponse = {
  data: EducationLevelCount[];
} & CommonAPIResponse;

export type AvgYearsCodingByLocation = {
  AvgYearsCoding: number;
  Location: string;
} & GenericCount;

export type APIAvgYearsCodingByLocationResponse = {
  data: AvgYearsCodingByLocation[];
} & CommonAPIResponse;

export type YearsCodingGroupResponse = {
  data: Array<
    {
      YearsCodingGroup: "0-1" | "1-4" | "5-9" | "10-20" | "Over 20";
    } & GenericCount
  >;
};

export type APIYearsCodingGroupResponse =
  GenericAPIResponse<YearsCodingGroupResponse>;

export interface AvgYearsCodingByDeveloperType {
  data: Array<
    {
      AvgYearsCoding: number;
      DeveloperTypeName: string;
    } & GenericCount
  >;
}

export type APIAvgYearsCodingByDeveloperTypeResponse =
  GenericAPIResponse<AvgYearsCodingByDeveloperType>;

export type LearningResource = {
  data: Array<
    {
      AgeGroup?: AgeGroupType;
      ResourceName: string;
      ResourceType: string;
    } & GenericCount
  >;
};

export type APILearningResourcesResponse = GenericAPIResponse<LearningResource>;

export type APICompaniesResponse = GenericAPIResponse<
  {
    data: Array<{
      country: string;
      id: number;
      industry: string;
      name: string;
      profit: number;
      projects: Array<{
        budget: number;
        description: string;
        duration: number;
        id: number;
        name: string;
      }>;
    }>;
  } & {
    total_pages: number;
  }
>;

export type CompanyNameType =
  | "CompanyName"
  | "RemotePolicy"
  | "WorkingTime"
  | "DeveloperTypeName";

export type APIRemotePolicyResponse = GenericAPIResponse<{
  data: Array<
    {
      Location?: string;
      RemotePolicy?: string;
      CompanyName?: CompanyNameType;
      WorkingTime?: string;
      DeveloperTypeName?: string;
    } & GenericCount
  >;
}>;

export type APITechSalaryResponse = GenericAPIResponse<{
  data: Array<{
    AvgSalary: number;
    TechName?: string;
    DeveloperTypeName?: string;
  }>;
}>;

export type APITechnologiesResponse = GenericAPIResponse<
  {
    data: Array<{
      dateOfRelease: string;
      id: number;
      name: string;
      type: string;
      useCases: string;
    }>;
  } & {
    total_pages: number;
  }
>;

export type APIToolsResponse = GenericAPIResponse<
  {
    data: Array<{
      dateOfRelease: string;
      id: number;
      name: string;
      primaryPurposes: string;
      sync: string;
      type: string;
    }>;
  } & {
    total_pages: number;
  }
>;

export type APITechResourcesResponse = GenericAPIResponse<{
  data: Array<{
    ResourceNames: string[];
    TechName: string;
  }>;
}>;

export type APIToolResourcesResponse = GenericAPIResponse<{
  data: Array<{
    ResourceNames: string[];
    ToolName: string;
  }>;
}>;

export type APITechCountResponse = GenericAPIResponse<{
  data: Array<
    {
      TechName: string;
    } & GenericCount
  >;
}>;
