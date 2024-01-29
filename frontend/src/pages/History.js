import React from 'react';

const sales = [
    {
        buyerName: 'John Doe',
        productName: 'Product A',
        quantity: 2,
        price: 10,
        date: '2022-01-01',
        total: 20,
    },
    {
        buyerName: 'Jane Smith',
        productName: 'Product B',
        quantity: 1,
        price: 15,
        date: '2022-01-02',
        total: 15,
    },
    // Add more sales data here...
];

const History = () => {
    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold mb-4">Sales History</h1>
            <table className="min-w-full bg-white border border-gray-300">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">Buyer Name</th>
                        <th className="py-2 px-4 border-b">Product Name</th>
                        <th className="py-2 px-4 border-b">Quantity</th>
                        <th className="py-2 px-4 border-b">Price</th>
                        <th className="py-2 px-4 border-b">Date</th>
                        <th className="py-2 px-4 border-b">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {sales.map((sale, index) => (
                        <tr key={index}>
                            <td className="py-2 px-4 border-b">{sale.buyerName}</td>
                            <td className="py-2 px-4 border-b">{sale.productName}</td>
                            <td className="py-2 px-4 border-b">{sale.quantity}</td>
                            <td className="py-2 px-4 border-b">{sale.price}</td>
                            <td className="py-2 px-4 border-b">{sale.date}</td>
                            <td className="py-2 px-4 border-b">{sale.total}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default History;
