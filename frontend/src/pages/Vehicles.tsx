import React, { useState, useMemo, useEffect } from "react";
import { Search, Filter } from "lucide-react";
import { format } from "date-fns";
import { mockVehicles } from "../data/mockData";

const Vehicles: React.FC = () => {
  const [challans, setChallans]: any = useState([]);
  const [vehicles, setVehicles]: any = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    fetch("http://192.168.58.4:8000/api/rto/vehicles", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        rto_id: localStorage.getItem("rto_id") || 0,
      }),
    })
      .then((res) => res.json())
      .then((data) => setVehicles(data.vehicles));
  }, []);

  const types = useMemo(
    () => Array.from(new Set(mockVehicles.map((v) => v.type))),
    []
  );

  const filteredVehicles = vehicles
  //
  // useMemo(() => {
  //   return vehicles.filter((vehicle: any) => {
  //     const matchesSearch =
  //       vehicle.vehicle_vin.toLowerCase().includes(searchTerm.toLowerCase()) ||
  //       (vehicle.vehicle_owner_name &&
  //         vehicle.vehicle_metadata.owner_name
  //           .toLowerCase()
  //           .includes(searchTerm.toLowerCase()));
  //     // .toLowerCase().includes(searchTerm.toLowerCase());
  //
  //     const matchesType = typeFilter === "all" || vehicle.type === typeFilter;
  //     const matchesStatus =
  //       statusFilter === "all" || vehicle.status === statusFilter;
  //
  //     return matchesSearch && matchesType && matchesStatus;
  //   });
  // }, [searchTerm, typeFilter, statusFilter, challans]);
  //
  const paginatedVehicles = useMemo(() => {
    const start = (currentPage - 1) * rowsPerPage;
    return filteredVehicles.slice(start, start + rowsPerPage);
  }, [filteredVehicles, currentPage, rowsPerPage]);

  const totalPages = Math.ceil(filteredVehicles.length / rowsPerPage);

  if (vehicles)
    return (
      <div className="p-6">
        <div className="flex flex-col gap-6 mb-6">
          <h1 className="text-2xl font-bold">Registered Vehicles</h1>

          <div className="flex flex-wrap gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search vehicles..."
                className="pl-10 pr-4 py-2 w-full border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            <div className="flex gap-4">
              <select
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
                className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="all">All Types</option>
                {types.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="suspended">Suspended</option>
                <option value="expired">Expired</option>
              </select>

              <select
                value={rowsPerPage}
                onChange={(e) => {
                  setRowsPerPage(Number(e.target.value));
                  setCurrentPage(1);
                }}
                className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value={10}>10 rows</option>
                <option value={20}>20 rows</option>
                <option value={50}>50 rows</option>
                <option value={filteredVehicles.length}>All</option>
              </select>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Vehicle Number
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Owner
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Registration Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Insurance Expiry
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {paginatedVehicles.map((vehicle: any) => (
                <tr key={vehicle.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {vehicle.vehicle_vin}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {"Truck"}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {vehicle.vehicle_owner_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {/* {format(new Date(vehicle.registrationDate), 'PP')} */}
                    {format(new Date(), "PP")}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {/* {format(new Date(vehicle.insuranceExpiry), 'PP')} */}
                    {format(new Date(), "PP")}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        // vehicle.status === 'active'
                        true
                          ? "bg-green-100 text-green-800"
                          : vehicle.status === "suspended"
                            ? "bg-red-100 text-red-800"
                            : "bg-yellow-100 text-yellow-800"
                        }`}
                    >
                      {"Active"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {totalPages > 1 && (
          <div className="mt-6 flex justify-center gap-2">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 border rounded-lg disabled:opacity-50"
            >
              Previous
            </button>
            <span className="px-4 py-2">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="px-4 py-2 border rounded-lg disabled:opacity-50"
            >
              Next
            </button>
          </div>
        )}
      </div>
    );
  return (
    <div>loading...</div>

  )
};

export default Vehicles;
