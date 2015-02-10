(defvar my-base-backup-dir "E:/Blair/EmacsBackups/")


; save old backup function
(fset 'orthodox-make-backup-file-name
      (symbol-function 'make-backup-file-name))

; create a new one
(defun make-bak (file)
  "Intended for (fset 'make-backup-file-name 'make-bak)."
  (let* ((file-dir (abbreviate-file-name (or (file-name-directory file)
                                                  default-directory)))
         ;; Using default-directory is necessary there because
         ;; 'file-name-directory returns nil on a relative path. 
         (backup-dir "")
         (file (file-name-nondirectory file))
         (backup-file "")
         (limit 0))
    (setq file-dir (expand-file-name file-dir))
    (if (string-match "^\\([Hh]:\\|[~]\\)\\(.*\\)" file-dir)
        (progn
          (setq file-dir (format "home/bconrad%s" 
                                 (match-string 2 file-dir)))))
    (if (string-match "^\\([A-Za-z]\\):\\(.*\\)" file-dir)
        (progn
          (setq file-dir (format "%s_%s" 
                                 (match-string 1 file-dir)
                                 (match-string 2 file-dir)))))
    
    
    (setq backup-dir (concat (expand-file-name my-base-backup-dir)
                             file-dir))
    
    ;; If the backup-dir doesn't exist, create it and all nonexistent
    ;; parents.
    (or (file-directory-p backup-dir)
        (make-directory backup-dir t))

    (concat backup-dir file "~")))

(defun use-original-backup ()
  (interactive)
  (fset 'make-backup-file-name 'orthodox-make-backup-file-name))

(defun use-my-backup ()
  (interactive)
  (fset 'make-backup-file-name 'make-bak))

(use-my-backup)


(provide 'my-backup)

