import React from 'react';

const Sidebar = () => {
    return (
        <div className="bg-gray-800 text-white h-screen w-64 flex flex-col justify-between">
            <div className="p-4">
                <h1 className="text-2xl font-bold">My Sidebar</h1>
            </div>
            <div className="flex flex-col space-y-4 p-4">
                <a href="/" className="text-gray-300 hover:text-white">Home</a>
                <a href="products" className="text-gray-300 hover:text-white">Products</a>
                <a href="history" className="text-gray-300 hover:text-white">History</a>
            </div>
            <div className="p-4">
                <p className="text-gray-300">© 2022 My Company</p>
            </div>
        </div>
    );
};

export default Sidebar;
