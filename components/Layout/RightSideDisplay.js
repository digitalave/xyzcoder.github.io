
import React, { PropTypes } from 'react';
import GoogleAd from './GoogleAd';

class RightSideDisplay extends React.Component {

  componentDidMount() {
    console.log("sidemenu component loaded");
    
  }

  componentWillUnmount() {
    
  }

  render() {

    const ad_unit_3 = {
      width: '100%',
      height: '90px'
    };

    return (
      <div class="col-lg-2 col-md-10 sideMenuSocialMedia">
        <GoogleAd client="ca-pub-3300393120826046" slot="7931356610" format="auto" wrapperDivStyle={style} />
        <br />
        <br />
        <GoogleAd client="ca-pub-3300393120826046" slot="7931356610" format="auto" wrapperDivStyle={style} />
     </div>
    );
  }
}

export default RightSideDisplay;
