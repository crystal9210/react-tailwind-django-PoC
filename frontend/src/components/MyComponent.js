import React, { useState, useEffect } from 'react';

const MyComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    setTimeout(() => {
      setData('This is data loaded asynchronously!');
    }, 2000); // Simulate an async operation
  }, []);

  return (
    <div>
      {data ? data : 'Loading data...'}
    </div>
  );
};

export default MyComponent;
