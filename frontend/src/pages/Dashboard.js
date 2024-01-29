import React from 'react';
import Sidebar from '../components/Sidebar';
import NewProduct from '../components/NewProduct';

const Dashboard = () => {
    return (
        <div className="flex flex-col h-screen bg-gray-100">
            <header className="bg-white shadow">
                Dashboard
            </header>
            <main className="flex-grow p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* <Sidebar /> */}
                    <NewProduct />
                </div>
            </main>
            <footer className="bg-white shadow">
                {/* Add your footer content here */}
            </footer>
        </div>
    );
};

export default Dashboard;
