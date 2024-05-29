import React, { useState, useEffect } from 'react';

const Component1 = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    setTimeout(() => {
      setData('This is the data of Component1 in the edit page that is loaded asynchronously!');
    }, 2000); // Simulate an async operation
  }, []);

  return (
    <div>
      {data ? data : 'Loading data...'}
    </div>
  );
};

export default Component1;
