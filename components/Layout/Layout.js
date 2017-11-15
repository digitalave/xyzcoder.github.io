/**
 * xyzcoder.github.io
 * https://github.com/kriasoft/react-static-boilerplate
 *
 * Copyright © 2015-present Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React, { PropTypes } from 'react';
import cx from 'classnames';
import Header from './Header';
import Footer from '../Footer';
import s from './Layout.css';
import SideMenu from './SideMenu';
import CustomSearch from './CustomSearch';
import Post from './Post';
import RightSideDisplay from './RightSideDisplay';
import PostList from "./PostList";

class Layout extends React.Component {

  static propTypes = {
    className: PropTypes.string,
  };

  componentDidMount() {
    
  }

  componentWillUnmount() {
    
  }

  render() {

    var page;
    if(props.page && props.page=="postlist"){
      page = <PostList />;
    }
    else{
      page = <Post postId={this.props.postId}/>;
    }

    return (
      <div>
          <Header />
          <CustomSearch />
            <div className="container-fluid">
              <div className="row">
                  <div className="col-lg-12 col-md-10">
                      <div className="row">

                        <div className="col-lg-10 col-md-10">
                          <div className="row">
                            <SideMenu />
                            {page}
                          </div>
                        </div>
                        <div className="col-lg-2 col-md-10">
                          <div className="row">
                            <RightSideDisplay />
                          </div>
                        </div>
                      </div>
                  </div>
              </div>
            </div>
          <Footer />
      </div>
    );
  }
}

export default Layout;
