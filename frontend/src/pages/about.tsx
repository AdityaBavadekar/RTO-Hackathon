import React from "react";
import { MapPin, Phone, Mail, Globe, Clock } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

const About: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-8">About RTO Office</h1>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-6">{user.rto_name}</h2>

        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <MapPin className="w-5 h-5 text-red-600 mt-1" />
            <div>
              <h3 className="font-medium">Address</h3>
              <p className="text-gray-600">{user.rto_address}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Phone className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Contact</h3>
              <p className="text-gray-600">{user.rto_contact_number}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Mail className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Email</h3>
              <p className="text-gray-600">{user.rto_main_email}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Globe className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Website</h3>
              <p className="text-gray-600">{user.rto_website}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Clock className="w-5 h-5 text-red-600" />
            <div>
              <h3 className="font-medium">Office Hours</h3>
              <p className="text-gray-600">{user.rto_office_hours}</p>
            </div>
          </div>
        </div>

        <div className="mt-8">
          <h3 className="font-medium mb-3">Services Offered</h3>
          <ul className="list-disc list-inside space-y-2 text-gray-600">
            {user.rto_metadata && user.rto_metadata.services && user.rto_metadata.services.map((service, index) => (
              <li key={index}>{service}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default About;
