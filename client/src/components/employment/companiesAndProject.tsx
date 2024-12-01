import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import { getCompaniesAndProjects } from "../../api";
import { APICompaniesResponse } from "../../api/interfaces";
import { useNavigate } from "react-router-dom";

const CompaniesAndProject: React.FC = () => {
  const [data, setData] = useState<APICompaniesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [filter, setFilter] = useState<string>("name");
  const [filterValue, setFilterValue] = useState<string>("");
  const navigate = useNavigate();

  const fetchData = async (
    page: number,
    filter: string,
    filterValue: string
  ) => {
    setLoading(true);
    try {
      const response = await getCompaniesAndProjects(page, filter, filterValue);
      setData(response);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchData(page, filter, filterValue);
    }, 1000);

    return () => clearTimeout(delayDebounceFn);
  }, [page, filter, filterValue]);

  return (
    <Box sx={{ p: 2 }}>
      <Button
        variant="contained"
        color="secondary"
        onClick={() => navigate("/employment")}
        sx={{ mb: 4 }}
      >
        Back to Employment
      </Button>
      <Typography variant="h4" gutterBottom>
        Companies and Projects
      </Typography>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="filter-label">Filter By</InputLabel>
        <Select
          labelId="filter-label"
          id="filter"
          value={filter}
          label="Filter By"
          onChange={(e) => setFilter(e.target.value as string)}
        >
          <MenuItem value="name">Name</MenuItem>
          <MenuItem value="minProfit">Min Profit</MenuItem>
          <MenuItem value="maxProfit">Max Profit</MenuItem>
          <MenuItem value="industry">Industry</MenuItem>
          <MenuItem value="country">Country</MenuItem>
        </Select>
      </FormControl>
      <TextField
        fullWidth
        label="Filter Value"
        value={filterValue}
        onChange={(e) => setFilterValue(e.target.value)}
        sx={{ mb: 2 }}
      />
      {loading && <Typography>Loading...</Typography>}
      {!loading && data && (
        <>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Company Name</TableCell>
                  <TableCell>Country</TableCell>
                  <TableCell>Industry</TableCell>
                  <TableCell>Profit</TableCell>
                  <TableCell>Projects</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.data.map((company) => (
                  <TableRow key={company.id}>
                    <TableCell>{company.name}</TableCell>
                    <TableCell>{company.country}</TableCell>
                    <TableCell>{company.industry}</TableCell>
                    <TableCell>{company.profit}</TableCell>
                    <TableCell>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>Project Name</TableCell>
                            <TableCell>Budget</TableCell>
                            <TableCell>Duration (months)</TableCell>
                            <TableCell>Description</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {company.projects.map((project) => (
                            <TableRow key={project.id}>
                              <TableCell>{project.name}</TableCell>
                              <TableCell>{project.budget}</TableCell>
                              <TableCell>{project.duration}</TableCell>
                              <TableCell>{project.description}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
            <FormControl sx={{ minWidth: 120 }}>
              <InputLabel id="page-label">Page</InputLabel>
              <Select
                labelId="page-label"
                id="page"
                value={page}
                label="Page"
                onChange={(e) => setPage(Number(e.target.value))}
              >
                {Array.from({ length: data.total_pages }, (_, i) => i + 1).map(
                  (pageNum) => (
                    <MenuItem key={pageNum} value={pageNum}>
                      {pageNum}
                    </MenuItem>
                  )
                )}
              </Select>
            </FormControl>
          </Box>
        </>
      )}
    </Box>
  );
};

export default CompaniesAndProject;
