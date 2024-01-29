import React, { useState } from 'react';
import axios from 'axios';

const NewProduct = () => {
    const [name, setName] = useState('');
    const [quantity, setQuantity] = useState(0);
    const [price, setPrice] = useState(0);

    const handleNameChange = (e) => {
        setName(e.target.value);
    };

    const handleQuantityChange = (e) => {
        setQuantity(e.target.value);
    };

    const handlePriceChange = (e) => {
        setPrice(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('/api/home', {
                "name": name,
                "qty": quantity,
                "price": price,
            });

            console.log(response.data);
            // Handle success
        } catch (error) {
            console.error(error);
            // Handle error
        }
    };

    return (
        <div>
            <h1>New Product</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Name:
                    <input type="text" id='name' value={name} onChange={handleNameChange} />
                </label>
                <br />
                <label>
                    Quantity:
                    <input type="number" id='quantity' value={quantity} onChange={handleQuantityChange} />
                </label>
                <br />
                <label>
                    Price:
                    <input type="number" id='price' value={price} onChange={handlePriceChange} />
                </label>
                <br />
                <button type="submit">Add Product</button>
            </form>
        </div>
    );
};

export default NewProduct;
