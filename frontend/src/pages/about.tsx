import React from "react";
import { MapPin, Phone, Mail, Globe, Clock } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

const About: React.FC = () => {
  const { user } = useAuth();

  const rtoInfo = {
    Mumbai: {
      name: "Mumbai RTO (MH-04)",
      address:
        "4th Floor, New Administrative Building, Government Colony, Bandra East, Mumbai - 400051",
      phone: "+91 22 2656 4000",
      email: "rto.mumbai@gov.in",
      website: "www.transport.maharashtra.gov.in",
      timings: "Monday to Friday: 10:00 AM to 5:30 PM",
      services: [
        "Vehicle Registration",
        "Driving License",
        "Vehicle Fitness Certificate",
        "Permit Issuance",
        "Tax Collection",
      ],
    },
  }[user?.area || "Mumbai"];

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-8">About RTO Office</h1>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-6">{rtoInfo.name}</h2>

        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <MapPin className="w-5 h-5 text-red-600 mt-1" />
            <div>
              <h3 className="font-medium">Address</h3>
              <p className="text-gray-600">{rtoInfo.address}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Phone className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Contact</h3>
              <p className="text-gray-600">{rtoInfo.phone}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Mail className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Email</h3>
              <p className="text-gray-600">{rtoInfo.email}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Globe className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Website</h3>
              <p className="text-gray-600">{rtoInfo.website}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Clock className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Office Hours</h3>
              <p className="text-gray-600">{rtoInfo.timings}</p>
            </div>
          </div>
        </div>

        <div className="mt-8">
          <h3 className="font-medium mb-3">Services Offered</h3>
          <ul className="list-disc list-inside space-y-2 text-gray-600">
            {rtoInfo.services.map((service, index) => (
              <li key={index}>{service}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default About;
