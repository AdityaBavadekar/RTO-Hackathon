import React from 'react';
import { format } from 'date-fns';
import { FileText, MapPin, AlertCircle } from 'lucide-react';
import type { Challan } from '../types';

interface ChallanListProps {
  challans: Challan[];
}

const ChallanList: React.FC<ChallanListProps> = ({ challans }) => {
  return (
    <div className="space-y-4">
      {challans.map((challan) => (
        <div key={challan.id} className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-semibold">{challan.vehicleNumber}</h3>
              <div className="flex items-center gap-2 text-gray-600 mt-1">
                <MapPin className="h-4 w-4" />
                <span>{challan.location.area}</span>
              </div>
            </div>
            <div className={`px-3 py-1 rounded-full ${
              challan.status === 'paid' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {challan.status.charAt(0).toUpperCase() + challan.status.slice(1)}
            </div>
          </div>
          
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Date</p>
              <p className="font-medium">{format(new Date(challan.date), 'PPP')}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Amount</p>
              <p className="font-medium">₹{challan.amount}</p>
            </div>
          </div>

          <div className="mt-4">
            <p className="text-sm text-gray-600">Violation</p>
            <p className="mt-1">{challan.violation}</p>
          </div>

          {challan.images.length > 0 && (
            <div className="mt-4">
              <p className="text-sm text-gray-600 mb-2">Evidence</p>
              <div className="flex gap-2 overflow-x-auto">
                {challan.images.map((image, index) => (
                  <img
                    key={index}
                    src={image}
                    alt={`Evidence ${index + 1}`}
                    className="h-20 w-20 object-cover rounded"
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ChallanList;