"""
OCR Text Detection API Contract

This contract defines the interface for detecting text in window captures.
Implements FR-009, FR-010, FR-011.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class TextRegion:
    """Represents detected text with location and confidence."""
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: int  # 0-100
    capture_timestamp: datetime
    window_handle: int
    
    @property
    def center_x(self) -> int:
        """Center X coordinate for clicking."""
        return self.x + self.width // 2
    
    @property
    def center_y(self) -> int:
        """Center Y coordinate for clicking."""
        return self.y + self.height // 2
    
    @property
    def area(self) -> int:
        """Bounding box area."""
        return self.width * self.height


class OCRTimeoutError(Exception):
    """Raised when OCR processing exceeds timeout threshold."""
    pass


class OCREngine:
    """Interface for OCR text detection in window captures."""
    
    def __init__(
        self,
        min_confidence: int = 60,
        language: str = "eng",
        psm_mode: int = 6
    ):
        """
        Initialize OCR engine with configuration.
        
        Args:
            min_confidence: Minimum confidence threshold (0-100) to return results
            language: Tesseract language code ("eng", "fra", "deu", etc.)
            psm_mode: Page Segmentation Mode (6=uniform text block, 11=sparse text)
        
        Example:
            # Initialize for game UI text (uniform blocks like buttons)
            ocr = OCREngine(min_confidence=70, language="eng", psm_mode=6)
        """
        raise NotImplementedError
    
    def detect_text(
        self,
        image: np.ndarray,
        window_handle: int,
        roi: Optional[Tuple[int, int, int, int]] = None,
        timeout_seconds: float = 5.0
    ) -> List[TextRegion]:
        """
        Detect all text regions in an image.
        
        Args:
            image: Input image as NumPy array (BGR or grayscale)
            window_handle: Source window handle for TextRegion metadata
            roi: Optional region of interest (x, y, width, height) to search within
            timeout_seconds: Maximum time to wait for OCR completion
        
        Returns:
            List of TextRegion objects (empty if no text found above min_confidence)
        
        Raises:
            OCRTimeoutError: If OCR processing exceeds timeout
            ValueError: If image is invalid (wrong shape, empty)
        
        Example:
            # Detect all text in full capture
            regions = ocr.detect_text(capture.image, handle)
            for region in regions:
                print(f"Found '{region.text}' at ({region.x}, {region.y})")
            
            # Detect text only in bottom area (e.g., buttons at bottom 20% of screen)
            roi = (0, int(1080 * 0.8), 1920, int(1080 * 0.2))
            regions = ocr.detect_text(capture.image, handle, roi=roi)
        
        Performance: <500ms for typical game window region
        
        Requirements: ≥95% accuracy on standard game UI text (SC-004)
        """
        raise NotImplementedError
    
    def find_text(
        self,
        image: np.ndarray,
        search_text: str,
        window_handle: int,
        exact_match: bool = False,
        roi: Optional[Tuple[int, int, int, int]] = None,
        timeout_seconds: float = 5.0
    ) -> Optional[TextRegion]:
        """
        Find a specific text string in an image.
        
        Args:
            image: Input image
            search_text: Text to search for (case-insensitive unless exact_match=True)
            window_handle: Source window handle
            exact_match: If True, requires exact match; if False, substring match
            roi: Optional region of interest
            timeout_seconds: Maximum time to wait
        
        Returns:
            First TextRegion matching search_text, or None if not found
        
        Example:
            # Find "BATTLE" button
            battle_button = ocr.find_text(capture.image, "BATTLE", handle)
            if battle_button:
                print(f"BATTLE button at ({battle_button.center_x}, {battle_button.center_y})")
                # Can click at (battle_button.center_x, battle_button.center_y)
            
            # Find text containing "claim" (case-insensitive substring)
            claim_btn = ocr.find_text(capture.image, "claim", handle, exact_match=False)
        
        Use Case: Locate specific UI element by text for clicking
        """
        raise NotImplementedError
    
    def find_all_text(
        self,
        image: np.ndarray,
        search_text: str,
        window_handle: int,
        exact_match: bool = False,
        roi: Optional[Tuple[int, int, int, int]] = None,
        timeout_seconds: float = 5.0
    ) -> List[TextRegion]:
        """
        Find all occurrences of specific text in an image.
        
        Args:
            image: Input image
            search_text: Text to search for
            window_handle: Source window handle
            exact_match: Exact or substring match
            roi: Optional region of interest
            timeout_seconds: Maximum time to wait
        
        Returns:
            List of all TextRegions matching search_text
        
        Example:
            # Find all "CLAIM" buttons on screen (multi-reward claim scenario)
            claim_buttons = ocr.find_all_text(capture.image, "CLAIM", handle)
            print(f"Found {len(claim_buttons)} claim buttons")
            for btn in claim_buttons:
                # Click each one
                click_handler.click_at(btn.center_x, btn.center_y, handle)
        """
        raise NotImplementedError
    
    def preprocess_for_ocr(
        self,
        image: np.ndarray,
        enhance_contrast: bool = True,
        denoise: bool = False
    ) -> np.ndarray:
        """
        Preprocess image to improve OCR accuracy.
        
        Args:
            image: Input image (BGR or grayscale)
            enhance_contrast: Apply thresholding/adaptive histogram equalization
            denoise: Apply denoising filter (slower but better for noisy images)
        
        Returns:
            Preprocessed image (grayscale, thresholded)
        
        Example:
            # Manual preprocessing for difficult text
            preprocessed = ocr.preprocess_for_ocr(capture.image)
            regions = ocr.detect_text(preprocessed, handle)
        
        Use Case: When default OCR accuracy is low, try preprocessing first
        
        Notes:
            - Converts to grayscale
            - Applies binary threshold or adaptive threshold
            - Optionally applies Gaussian blur or morphological operations
        """
        raise NotImplementedError
    
    def set_confidence_threshold(self, min_confidence: int) -> None:
        """
        Update minimum confidence threshold for results.
        
        Args:
            min_confidence: New threshold (0-100)
        
        Example:
            # Lower threshold for difficult text
            ocr.set_confidence_threshold(50)
            regions = ocr.detect_text(capture.image, handle)
            # Now includes lower-confidence results
        """
        raise NotImplementedError
