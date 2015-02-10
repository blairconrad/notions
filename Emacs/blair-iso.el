;;; BLAIR-ISO.EL --- easily enter iso-accented sequence

;; Copyright (C) 2000 Blair Conrad

;; Author: Blair Conrad bconrad@mitra.com
;; Maintainer: Blair Conrad bconrad@mitra.com
;; Created: 26 Apr 2000
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
;; blair-iso|Blair Conrad|bconrad@mitra.com
;; |easily enter iso-accented sequence
;; |$Date: 2006/02/24 15:54:44 $|$Revision: 1.1 $|~/packages/blair-iso.el

;;; Commentary:

;;; Change log:
;; $Log: blair-iso.el,v $
;; Revision 1.1  2006/02/24 15:54:44  bconrad
;; initial revision
;;
;; Revision 1.1  2003/05/06 19:26:43  bconrad
;; - initial revision
;;
;; Revision 1.1.1.1  2003/05/06 18:48:11  bconrad
;; imported sources
;;
;; Revision 1.2  2000/06/09 18:34:43  bconrad
;; - use save-restriction and narrow-to-region to ensure that
;;   cursor is placed after the inserted characters
;;
;; Revision 1.1  2000/04/26 16:56:19  bconrad
;; Initial revision
;;

;;; Code:

(defconst blair-iso-version (substring "$Revision: 1.1 $" 11 -2)
  "$Id: blair-iso.el,v 1.1 2006/02/24 15:54:44 bconrad Exp $

Report bugs to: Blair Conrad bconrad@mitra.com")


(require 'iso-acc)

(defun blair-iso-accentuate ()
  "* Enter an iso-accentuated sequence."
  (interactive)
  (let ((seq (read-input "Sequence: ")))
    (save-restriction
     (narrow-to-region (point) (point))
     (insert seq)
     (iso-accentuate (point-min) (point-max))
     (goto-char (point-max)))))



;;; BLAIR-ISO.EL ends here
