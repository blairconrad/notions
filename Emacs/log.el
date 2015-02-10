;;; log-mode.el --- log code editing commands for Emacs

;;; Copyright (C) 2001 Blair Conrad
;; Author: Blair Conrad
;; <blair.conrad@mitra.com>, with much inspiration taken from Andrew
;; Csillag's <drew_csillag@geocities.com> m4-mode.  Maintainer: Blair
;; Conrad <blair.conrad@mitra.com> Keywords: languages, faces

;; This file is NOT part of GNU Emacs.

;; GNU Emacs is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2, or (at your option)
;; any later version.

;; GNU Emacs is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file COPYING.  If not, write to the
;; Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.

;;; Commentary:

;; A smart viewing mode for Mitra log files.  It sets the font-lock
;; syntax stuff for colorization

;;; Code:

(defgroup log nil
  "log editing commands for Emacs."
  :prefix "log-"
  :group 'languages)


(defvar log-debug-face 'log-debug-face "Face name to use for debug lines")
(defface log-debug-face
  `((((background light)) (:slant italic :underline t :foreground "red"))
    (((background dark)) (:slant italic :underline t)))
  "Face for debug lines"
  :group 'log)

(defvar log-info-face 'log-info-face "Face name to use for info lines")
(defface log-info-face
  `((((background light)) (:slant italic :underline t :foreground "red"))
    (((background dark)) (:slant italic :underline t)))
  "Face for info lines"
  :group 'log)

(defvar log-warning-face 'log-warning-face "Face name to use for warning lines")
(defface log-warning-face
  `((((background light)) (:slant italic :underline t :foreground "red"))
    (((background dark)) (:slant italic :underline t)))
  "Face for warning lines"
  :group 'log)

(defvar log-error-face 'log-error-face "Face name to use for error lines")
(defface log-error-face
  `((((background light)) (:slant italic :underline t :foreground "red"))
    (((background dark)) (:slant italic :underline t)))
  "Face for error lines"
  :group 'log)

(defvar log-audit-face 'log-audit-face "Face name to use for audit lines")
(defface log-audit-face
  `((((background light)) (:slant italic :underline t :foreground "red"))
    (((background dark)) (:slant italic :underline t)))
  "Face for audit lines"
  :group 'log)

(defvar log-fatal-face 'log-fatal-face "Face name to use for fatal lines")
(defface log-fatal-face
  `((((background light)) (:slant italic :underline t :foreground "red"))
    (((background dark)) (:slant italic :underline t)))
  "Face for fatal lines"
  :group 'log)

;;
;; The \\(2[0-9]\\|1\\) is like that 'cos Broker thinks it's the year
;; 102, as I write this.
;;
(defvar log-font-lock-keywords
  '(
    ("^INFO..?2[0-9][0-9][0-9].*" . log-info-face)
    ("^I.\\(2[0-9]\\|1\\)[0-9][0-9].*" . log-info-face)
    ("^A.\\(2[0-9]\\|1\\)[0-9][0-9].*" . log-audit-face)
    ("^AUDIT.2[0-9][0-9][0-9].*" . log-audit-face)
    ("^E.\\(2[0-9]\\|1\\)[0-9][0-9].*" . log-error-face)
    ("^ERROR.2[0-9][0-9][0-9].*" . log-error-face)
    ("^FATAL.2[0-9][0-9][0-9].*" . log-fatal-face)
    ("^\\(WARN\\)..?2[0-9][0-9][0-9].*" 1 log-warning-face)
    ("^\\(D\\).\\(2[0-9]\\|1\\)[0-9][0-9].*" 1  log-debug-face)
    ("^\\(DEBUG\\).2[0-9][0-9][0-9].*" 1  log-debug-face)
    )
  ) ; defvar

(defcustom log-mode-hook nil
  "*Hook called by `log-mode'."
  :type 'hook
  :group 'log)

;;;###autoload
(defun log-mode ()
  "A major mode to edit log macro files.
"
  (interactive)
  (kill-all-local-variables)

  (make-local-variable	'font-lock-defaults)  
  (setq major-mode 'log-mode
	mode-name "log"
	font-lock-defaults '(log-font-lock-keywords t)
	)
  (run-hooks 'log-mode-hook))

(provide 'log-mode)

;;; log.el ends here
