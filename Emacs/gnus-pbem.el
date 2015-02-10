
;;; GNUS-PBEM.EL --- aid replying to PBeM boards

;; Copyright (C) 2000 Blair Conrad

;; Author: Blair Conrad bconrad@mitra.com
;; Maintainer: Blair Conrad bconrad@mitra.com
;; Created: 10 Mar 2000
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
;; gnus-pbem|Blair Conrad|bconrad@mitra.com
;; |aid replying to PBeM boards
;; |$Date: 2006/02/24 15:54:44 $|$Revision: 1.1 $|~/packages/gnus-pbem.el

;;; Commentary:

;;; Change log:
;; $Log: gnus-pbem.el,v $
;; Revision 1.1  2006/02/24 15:54:44  bconrad
;; initial revision
;;
;; Revision 1.1  2003/05/06 19:26:47  bconrad
;; - initial revision
;;
;; Revision 1.1.1.1  2003/05/06 18:48:10  bconrad
;; imported sources
;;
;; Revision 1.5  2000/07/20 14:57:41  bconrad
;; - fixed messed up "move" string in multiple commands
;;
;; Revision 1.4  2000/07/13 18:21:09  bconrad
;; It was all messed up, so I fixed it.
;;
;; Revision 1.3  2000/04/24 13:12:49  bconrad
;; - improved replying to detect "multiple" responses separated by
;;   spaces, e.g.
;;      8-5,4 greedy
;; - started "require"ing gnus to get rid of nasty "not known to be
;;   defined" warning when byte-compiling
;;
;; Revision 1.2  2000/04/11 14:36:35  bconrad
;; Updated gnus-maybe-pbem-reply to use variables
;;      gnus-pbem-username
;;      gnus-pbem-password
;; instead of hardcoding them.
;;
;; Revision 1.1  2000/03/10 20:19:21  bconrad
;; Initial revision
;;

;;; Code:

(require 'gnus)
;(require 'string)

(defconst gnus-pbem-version (substring "$Revision: 1.1 $" 11 -2)
  "$Id: gnus-pbem.el,v 1.1 2006/02/24 15:54:44 bconrad Exp $

Report bugs to: Blair Conrad bconrad@mitra.com")

(defvar gnus-pbem-username "" 
  "*Username to be used when communicating with the PBeM server.")

(defvar gnus-pbem-password "" 
  "*Password to be used when communicating with the PBeM server.")

(defun gnus-maybe-pbem-reply ()
  "* Reply to a news article, either using the normal gnus-summary-reply
function (the default), or gnus-pbem-reply if the article looks like a
PBeM board."
  (interactive)
  (let (move game-name game-num)
    (beginning-of-line nil)
    (if (search-forward-regexp "\\(New\\s-+\\)?\\(\\S-+\\)\\s-+Board\\s-+\\(\\S-+\\)"
                               (point-max) t)
        (progn
          (setq game-name (match-string 2))
          (setq game-num (match-string 3))
          
          (setq move (read-input "Move: "))
          (gnus-pbem-reply game-name game-num move))
      (gnus-summary-reply))))

;;; Private functions ========================================================

(defun gnus-pbem-reply (game-name game-num move)
  "* Reply to a PBeM board"
  (gnus-summary-reply)
  (message-goto-subject)
  (beginning-of-line nil)
  (kill-line nil)
  (let 
      ((move-list nil))
    
    ;; This regexp is bad?
    (while (string-match "\\(^.*\\s-+\\|^\\)\\(\\S-+\\)\\s-*$" move)
      (setq move-list (cons (match-string 2 move) move-list))
      (setq move (match-string 1 move)))
    (if (cdr move-list)
        ;; move-list has a tail, so it must be a list of moves
        (gnus-multiple-reply game-name game-num move-list)
      (gnus-simple-reply game-name game-num (car move-list)))))

(defun gnus-simple-reply (game-name game-num move)
  (insert (format "Subject: %s move %s %s %s %s" 
                  game-name 
                  game-num 
                  gnus-pbem-username
                  gnus-pbem-password
                  move)))

(defun gnus-multiple-reply (game-name game-num move-list)
  (insert "Subject: multiple")
  ; go to body, insert each command
  (message-goto-body)
  (mapcar (lambda (move)
                 (insert (format "%s move %s %s %s %s\n"
                                 game-name 
                                 game-num 
                                 gnus-pbem-username
                                 gnus-pbem-password
                                 move)))
          move-list))
;;; GNUS-PBEM.EL ends here

