
import React from 'react';
import cx from 'classnames';
import SocialMediaList from './SocialMediaList';
import FacebookPage from './FacebookPage';
import RecentPosts from './RecentPosts';


class SideMenu extends React.Component {

  componentDidMount() {
    window.componentHandler.upgradeElement(this.root);
  }

  componentWillUnmount() {
    window.componentHandler.downgradeElements(this.root);
  }

  render() {
    return (
      <div className="col-lg-2 col-md-10 sideMenuSocialMedia">
          <SocialMediaList />

          <div className="nav-side-menu col-lg-2 col-md-2">
              
              <RecentPosts />

              <br/>
              <br/>
              <br/>

              <FacebookPage />

          </div>
      </div>
    );
  }
}

export default SideMenu;
