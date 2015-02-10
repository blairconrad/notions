;;; GNUS-SPAM.EL --- spam tools

;; Copyright (C) 2000 Blair Conrad (x2336)

;; Author: Blair Conrad (x2336) bconrad@mitra.com
;; Maintainer: Blair Conrad (x2336) bconrad@mitra.com
;; Created: 22 Mar 2000
;; Version: 1.0
;; Keywords:

 
;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 1, or (at your option)
;; any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; A copy of the GNU General Public License can be obtained from this
;; program's author (send electronic mail to bconrad@mitra.com) or
;; from the Free Software Foundation, Inc., 675 Mass Ave, Cambridge,
;; MA 02139, USA.

;; LCD Archive Entry:
;; gnus-spam|Blair Conrad (x2336)|bconrad@mitra.com
;; |spam tools
;; |$Date: 2006/02/24 15:54:45 $|$Revision: 1.1 $|~/packages/gnus-spam.el

;;; Commentary:

;;; Change log:
;; $Log: gnus-spam.el,v $
;; Revision 1.1  2006/02/24 15:54:45  bconrad
;; initial revision
;;
;; Revision 1.1  2003/05/06 19:26:47  bconrad
;; - initial revision
;;
;; Revision 1.1.1.1  2003/05/06 18:48:10  bconrad
;; imported sources
;;
;; Revision 1.3  2000/03/22 14:20:31  bconrad
;; Now preserves "---- end of forwarded message ----" line.
;; Inserts "I received this unsolicited mail" comment.
;;
;; Revision 1.2  2000/03/22 13:58:23  bconrad
;; better comments
;;

;;; Code:

(defconst gnus-spam-version (substring "$Revision: 1.1 $" 11 -2)
  "$Id: gnus-spam.el,v 1.1 2006/02/24 15:54:45 bconrad Exp $

Report bugs to: Blair Conrad (x2336) bconrad@mitra.com")

(defvar gnus-spam-user-full-name user-full-name
  "*Full name to be inserted in the abuse complaint. 
Defaults to user-full-name.")

(defvar gnus-spam-user-mail-address user-mail-address
  "*Mail address to be inserted in the abuse complaint. 
Defaults to user-mail-address.")



(defun gnus-spam-report-abuse()
  (interactive)
  (gnus-summary-beginning-of-article)
  (gnus-article-hide-headers -1)
  (other-window 1)
  (copy-region-as-kill (point-min) (point-max))
  (other-window 1)
  (gnus-summary-mail-forward)
  
  (beginning-of-line)
  (forward-line 3)
  (insert (format "\nI received the following unsolicited message.

        %s
        %s\n\n" gnus-spam-user-full-name gnus-spam-user-mail-address))
  (forward-line)

  (beginning-of-line)

  ;; save the point, move to the end of the buffer, up one line
  ;; (to leave the "------- End of forwarded message -------" line)
  ;; and remove the message that gnus inserts
  (let ((beg (point)))
    (end-of-buffer)
    (forward-line -1)
    (delete-region beg (point)))

  ;; paste in the copy of the message with all the headers
  (yank)

  ;; move to the end of the "To:" line
  (message-goto-to)
  (end-of-line)

  (insert "abuse@"))

;;; GNUS-SPAM.EL ends here
