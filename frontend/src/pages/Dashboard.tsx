import React, { useState, useMemo } from 'react';
import { Search, Filter, ChevronDown } from 'lucide-react';
import ChallanList from '../components/ChallanList';
import { mockChallans } from '../data/mockData';

const Dashboard: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'paid' | 'pending'>('all');
  const [areaFilter, setAreaFilter] = useState('all');
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);

  const areas = useMemo(() => 
    Array.from(new Set(mockChallans.map(c => c.location.area))),
    []
  );

  const filteredChallans = useMemo(() => {
    return mockChallans.filter(challan => {
      const matchesSearch = 
        challan.vehicleNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        challan.violation.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesStatus = statusFilter === 'all' || challan.status === statusFilter;
      const matchesArea = areaFilter === 'all' || challan.location.area === areaFilter;

      return matchesSearch && matchesStatus && matchesArea;
    });
  }, [searchTerm, statusFilter, areaFilter]);

  const paginatedChallans = useMemo(() => {
    const start = (currentPage - 1) * rowsPerPage;
    return filteredChallans.slice(start, start + rowsPerPage);
  }, [filteredChallans, currentPage, rowsPerPage]);

  const totalPages = Math.ceil(filteredChallans.length / rowsPerPage);

  return (
    <div className="p-6">
      <div className="flex flex-col gap-6 mb-6">
        <h1 className="text-2xl font-bold">Challan Records</h1>
        
        <div className="flex flex-wrap gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search challans..."
              className="pl-10 pr-4 py-2 w-full border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="flex gap-4">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as 'all' | 'paid' | 'pending')}
              className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="all">All Status</option>
              <option value="paid">Paid</option>
              <option value="pending">Pending</option>
            </select>

            <select
              value={areaFilter}
              onChange={(e) => setAreaFilter(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="all">All Areas</option>
              {areas.map(area => (
                <option key={area} value={area}>{area}</option>
              ))}
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
              <option value={filteredChallans.length}>All</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        <ChallanList challans={paginatedChallans} />
      </div>

      {totalPages > 1 && (
        <div className="mt-6 flex justify-center gap-2">
          <button
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="px-4 py-2 border rounded-lg disabled:opacity-50"
          >
            Previous
          </button>
          <span className="px-4 py-2">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="px-4 py-2 border rounded-lg disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default Dashboard;