import { Vehicle, Challan } from '../types';

export const mockVehicles: Vehicle[] = [
  {
    id: '1',
    number: 'MH 04 AB 1234',
    type: 'Car',
    owner: 'John Doe',
    registrationDate: '2023-01-15',
    insuranceExpiry: '2024-01-15',
    status: 'active'
  },
  {
    id: '2',
    number: 'MH 04 CD 5678',
    type: 'Truck',
    owner: 'Jane Smith',
    registrationDate: '2023-02-20',
    insuranceExpiry: '2024-02-20',
    status: 'active'
  },
  // Add more vehicles here...
];

export const mockChallans: Challan[] = Array.from({ length: 50 }, (_, index) => ({
  id: (index + 1).toString(),
  vehicleNumber: index % 2 === 0 ? 'MH 04 AB 1234' : 'MH 04 CD 5678',
  date: new Date(2024, 0, index + 1).toISOString(),
  location: {
    lat: 19.0760 + (Math.random() - 0.5) * 0.1,
    lng: 72.8777 + (Math.random() - 0.5) * 0.1,
    area: index % 2 === 0 ? 'Mumbai Central' : 'Bandra West'
  },
  violation: index % 3 === 0 
    ? 'Red Light Violation' 
    : index % 3 === 1 
    ? 'Missing Red Cross Mark' 
    : 'Speeding',
  amount: 1000 + (index % 3) * 500,
  status: index % 2 === 0 ? 'pending' : 'paid',
  images: [
    'https://images.unsplash.com/photo-1590361232060-61b9a025a068?auto=format&fit=crop&q=80&w=300&h=300',
  ],
  description: `Vehicle violation recorded at ${index % 2 === 0 ? 'Mumbai Central' : 'Bandra West'}`
}));