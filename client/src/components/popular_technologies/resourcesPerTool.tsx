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
} from "@mui/material";
import { getResourcesPerTool } from "../../api";
import { APIToolResourcesResponse } from "../../api/interfaces";
import { useNavigate } from "react-router-dom";

const ResourcesPerTool: React.FC = () => {
  const [data, setData] = useState<APIToolResourcesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await getResourcesPerTool();
      setData(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Box sx={{ p: 2 }}>
      <Button
        variant="contained"
        color="secondary"
        onClick={() => navigate("/popular_technologies")}
        sx={{ mb: 4 }}
      >
        Back to Popular Technologies
      </Button>
      <Typography variant="h4" gutterBottom>
        Resources Per Tool
      </Typography>
      {loading && <Typography>Loading...</Typography>}
      {!loading && data && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Tool Name</TableCell>
                <TableCell>Resource Names</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.data.map((toolResource) => (
                <TableRow key={toolResource.ToolName}>
                  <TableCell>{toolResource.ToolName}</TableCell>
                  <TableCell>{toolResource.ResourceNames.join(", ")}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default ResourcesPerTool;
