import {
  TelegramShareButton,
  WhatsappShareButton,
  EmailShareButton,
  VKShareButton,
} from "react-share";
import { useLocation } from "react-router-dom";
import divider from "../../assets/Divider2.svg";
import "./share.scss";
import tg from "../../assets/tg.svg";
import wapp from "../../assets/wapp.svg";
import mail from "../../assets/email.svg";
import vk from "../../assets/vk.svg";
export default function ShareButton() {
  const location = useLocation();
  const { pathname } = location;
  let shareUrl = "theconf.ru" + pathname;

  return (
    <>
      <div className="sharebutton">
        <h1>Поделиться</h1>
        <img src={divider} alt="" />
        <div className="sharebutton-social">
          <TelegramShareButton url={shareUrl}>
            <img src={tg} alt="telegram" />
          </TelegramShareButton>
          <WhatsappShareButton url={shareUrl}>
            <img src={wapp} alt="watsapp" />
          </WhatsappShareButton>
          <EmailShareButton url={shareUrl}>
            <img src={mail} alt="email" />
          </EmailShareButton>
          <VKShareButton url={shareUrl}>
            <img src={vk} alt="vk" />
          </VKShareButton>
        </div>
      </div>
    </>
  );
}
