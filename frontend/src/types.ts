export interface Challan {
  id: string;
  vehicleNumber: string;
  date: string;
  location: {
    lat: number;
    lng: number;
    area: string;
  };
  violation: string;
  amount: number;
  status: 'paid' | 'pending';
  images: string[];
  description: string;
}

export interface Vehicle {
  id: string;
  number: string;
  type: string;
  owner: string;
  registrationDate: string;
  insuranceExpiry: string;
  status: 'active' | 'suspended' | 'expired';
}

export interface AuthUser {
  id: string;
  name: string;
  area: string;
  role: 'admin' | 'officer';
}