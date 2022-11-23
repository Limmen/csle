import React from "react";
import './YoutubeEmbed.css';
import {HTTP_PREFIX} from "../../Common/constants";


/**
 * Component for embedding a youtube video on a page
 */
const YoutubeEmbed = (props) => (
    <div className="video-responsive su-youtube">
        <iframe
            width="853"
            height="480"
            src={`${HTTP_PREFIX}www.youtube.com/embed/${props.embedId}`}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            title="Embedded youtube"
        />
    </div>
);

YoutubeEmbed.propTypes = {};
YoutubeEmbed.defaultProps = {};
export default YoutubeEmbed;