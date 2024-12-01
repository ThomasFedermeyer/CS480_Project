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
  Select,
  MenuItem,
  TextField,
} from "@mui/material";
import { getTechnologies } from "../../api";
import { APITechnologiesResponse } from "../../api/interfaces";
import { useNavigate } from "react-router-dom";

const Technologies: React.FC = () => {
  const [data, setData] = useState<APITechnologiesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [filter, setFilter] = useState<string | null>(null);
  const [filterValue, setFilterValue] = useState<string | null>(null);
  const [sortOrder, setSortOrder] = useState<string | null>(null);
  const [sortType, setSortType] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchData = async (
    page: number,
    filter: string | null,
    filterValue: string | null,
    sortOrder: string | null,
    sortType: string | null
  ) => {
    setLoading(true);
    try {
      const response = await getTechnologies(
        page,
        filter,
        filterValue,
        sortOrder,
        sortType
      );
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchData(page, filter, filterValue, sortOrder, sortType);
    }, 1000);

    return () => clearTimeout(delayDebounceFn);
  }, [page, filter, filterValue, sortOrder, sortType]);

  useEffect(() => {
    setFilterValue(null);
    setSortOrder(null);
    setSortType(null);
  }, [filter]);

  return (
    <Box sx={{ p: 2 }}>
      <Button
        variant="contained"
        color="secondary"
        onClick={() => navigate("/")}
        sx={{ mb: 4 }}
      >
        Back to Home
      </Button>
      <Typography variant="h4" gutterBottom>
        Popular Technologies
      </Typography>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="filter-label">Filter By</InputLabel>
        <Select
          labelId="filter-label"
          id="filter"
          value={filter === null ? "" : filter}
          label="Filter By"
          onChange={(e) => setFilter(e.target.value as string)}
        >
          <MenuItem value="">No Selection</MenuItem>
          <MenuItem value="Sort">Sort</MenuItem>
          <MenuItem value="SortType">SortType</MenuItem>
          <MenuItem value="name">Name</MenuItem>
          <MenuItem value="type">Type</MenuItem>
        </Select>
      </FormControl>
      {filter === "Sort" && (
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="sortOrder-label">Sort Order</InputLabel>
          <Select
            labelId="sortOrder-label"
            id="sortOrder"
            value={sortOrder === null ? "" : sortOrder}
            label="Sort Order"
            onChange={(e) => setSortOrder(e.target.value as string)}
          >
            <MenuItem value="asc">ASC</MenuItem>
            <MenuItem value="desc">DESC</MenuItem>
          </Select>
        </FormControl>
      )}
      {filter === "SortType" && (
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="sortType-label">Sort Type</InputLabel>
          <Select
            labelId="sortType-label"
            id="sortType"
            value={sortType === null ? "" : sortType}
            label="Sort Type"
            onChange={(e) => setSortType(e.target.value as string)}
          >
            <MenuItem value="TechName">Tech Name</MenuItem>
            <MenuItem value="DateOfRelease">Date Of Release</MenuItem>
          </Select>
        </FormControl>
      )}
      {(filter === "name" || filter === "type") && (
        <TextField
          fullWidth
          label={filter === "name" ? "Name" : "Type"}
          value={filterValue === null ? "" : filterValue}
          onChange={(e) => setFilterValue(e.target.value)}
          sx={{ mb: 2 }}
        />
      )}
      {loading && <Typography>Loading...</Typography>}
      {!loading && data && (
        <>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Use Cases</TableCell>
                  <TableCell>Date of Release</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.data.map((tech) => (
                  <TableRow key={tech.id}>
                    <TableCell>{tech.name}</TableCell>
                    <TableCell>{tech.type}</TableCell>
                    <TableCell>{tech.useCases}</TableCell>
                    <TableCell>
                      {new Date(tech.dateOfRelease).toLocaleDateString()}
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

export default Technologies;
