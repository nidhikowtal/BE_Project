import './App.css';
import React from 'react';

import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBTextArea,
}
from 'mdb-react-ui-kit';

function App() {
  return (
    <MDBContainer fluid>

      <MDBRow className='d-flex justify-content-center align-items-center'>
        <MDBCol lg='9' className='my-5'>

          <h1 class="text-white mb-4">Enter the Jira Story</h1>

          <MDBCard>
            <MDBCardBody className='px-4'>
              <MDBRow className='align-items-center pt-4 pb-3'>

                <MDBCol md='3' className='ps-5'>
                  <h6 className="mb-0"></h6>
                </MDBCol>

                <MDBCol md='9' className='pe-5'>
                  <MDBTextArea id='textAreaExample' rows={3} />
                </MDBCol>

              </MDBRow>


              <button type="submit">
            Submit
          </button>

            </MDBCardBody>
          </MDBCard>

        </MDBCol>
      </MDBRow>

    </MDBContainer>
  );
}

export default App;




