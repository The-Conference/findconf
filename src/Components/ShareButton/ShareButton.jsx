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
import { useRef, useState } from "react";
import useOnClickOutside from "../Hooks/useOnClickOutside";
import share from "../../assets/share.svg";
export default function ShareButton() {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef(null);

  useOnClickOutside(ref, () => setIsOpen(false));

  const location = useLocation();
  const { pathname } = location;
  let shareUrl = "theconf.ru" + pathname;

  return (
    <>
      <img
        className="share"
        src={share}
        alt="share"
        onClick={() => setIsOpen(!isOpen)}
      />
      {isOpen && (
        <div className="sharebutton" ref={ref}>
          <div>
            <h1>Поделиться</h1>
            <svg
              onClick={() => setIsOpen(!isOpen)}
              width="14"
              height="14"
              viewBox="0 0 14 14"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M13.53 12.47C13.823 12.763 13.823 13.238 13.53 13.531C13.384 13.677 13.192 13.751 13 13.751C12.808 13.751 12.616 13.678 12.47 13.531L6.99999 8.061L1.52999 13.531C1.38399 13.677 1.19199 13.751 0.999993 13.751C0.807993 13.751 0.615994 13.678 0.469994 13.531C0.176994 13.238 0.176994 12.763 0.469994 12.47L5.94 7.00002L0.469994 1.53005C0.176994 1.23705 0.176994 0.762018 0.469994 0.469018C0.762994 0.176018 1.238 0.176018 1.531 0.469018L7.001 5.93905L12.471 0.469018C12.764 0.176018 13.239 0.176018 13.532 0.469018C13.825 0.762018 13.825 1.23705 13.532 1.53005L8.06199 7.00002L13.53 12.47Z"
                fill="#00002E"
              />
            </svg>
          </div>

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
      )}
    </>
  );
}