# app/information_gathering/osint/exiftool.py

import sys
import os
import subprocess
import json
import requests
from datetime import datetime
from urllib.parse import urlparse
import mimetypes

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class ExifTool:
    """Professional Metadata Extraction & Analysis Tool"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
        self.reports_dir = "reports/osint/exiftool"
        self.ensure_reports_dir()
        self.supported_formats = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic'],
            'Documents': ['.pdf', '.docx', '.xlsx', '.pptx', '.odt', '.ods'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
        }
    
    def ensure_reports_dir(self):
        """Create reports directory if not exists"""
        """Create reports directory if not exists"""
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def check_installation(self):
        """Check if exiftool is installed"""
        try:
            result = subprocess.run(['which', 'exiftool'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None
    
    def display_menu(self):
        """Display exiftool menu"""
        clear_screen()
        print_header("EXIFTOOL - METADATA EXTRACTION & ANALYSIS", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  Extract hidden metadata from files - GPS, camera info, software used,    ║{C_RESET}")
        print(f"{C_INFO}║  author details, timestamps, and more for forensic analysis.              ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        status = f"{C_OK}✓ Installed{C_RESET}" if self.tool_path else f"{C_ERR}✗ Not Installed{C_RESET}"
        print(f"{C_INFO}ExifTool Status: {status}{C_RESET}")
        print(f"{C_INFO}Reports Directory: {C_OK}{self.reports_dir}/{C_RESET}\n")
        
        print(f"{C_OK}1. Analyze Local File{C_RESET}        - Extract all metadata from single file")
        print(f"{C_OK}2. Analyze URL/Image{C_RESET}         - Download file from URL and analyze")
        print(f"{C_OK}3. Batch Analysis{C_RESET}            - Analyze multiple files from directory")
        print(f"{C_OK}4. GPS Location Extractor{C_RESET}    - Extract GPS coordinates from images")
        print(f"{C_OK}5. Camera/Device Info{C_RESET}        - Extract device and camera details")
        print(f"{C_OK}6. Author & Software{C_RESET}         - Find creator and software information")
        print(f"{C_OK}7. Timeline Analysis{C_RESET}         - Extract all date/time metadata")
        print(f"{C_OK}8. Metadata Removal{C_RESET}          - Remove all metadata from files")
        print(f"{C_OK}9. Supported Formats{C_RESET}         - View all supported file types")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def generate_report_header(self, report_type, filepath, scan_time=None):
        """Generate formatted report header"""
        if scan_time is None:
            scan_time = datetime.now()
        
        header = "=" * 80 + "\n"
        header += f"{report_type.upper().center(80)}\n"
        header += "=" * 80 + "\n\n"
        header += f"Analysis Tool:  ExifTool\n"
        header += f"Report Type:    {report_type}\n"
        header += f"Target File:    {filepath}\n"
        header += f"File Size:      {self.format_size(os.path.getsize(filepath)) if os.path.exists(filepath) else 'Unknown'}\n"
        header += f"Scan Date:      {scan_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "=" * 80 + "\n\n"
        
        return header
    
    def save_report(self, content, filename_prefix, filepath):
        """Save report to txt file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = os.path.basename(filepath)
        clean_name = os.path.splitext(base_filename)[0]
        
        report_filename = f"{filename_prefix}_{clean_name}_{timestamp}.txt"
        report_path = os.path.join(self.reports_dir, report_filename)
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            Logger.success(f"Report saved: {report_path}")
            return report_path
        except Exception as e:
            Logger.error(f"Failed to save report: {str(e)}")
            return None
    
    def analyze_local_file(self, filepath):
        """Analyze local file metadata"""
        if not os.path.exists(filepath):
            Logger.error(f"File not found: {filepath}")
            return
        
        clear_screen()
        print_header("FILE METADATA ANALYSIS", 80)
        
        scan_time = datetime.now()
        print(f"\n{C_OK}[*] Analyzing: {C_WARN}{filepath}{C_RESET}\n")
        
        # Basic file info
        file_size = os.path.getsize(filepath)
        file_ext = os.path.splitext(filepath)[1].lower()
        
        print(f"{C_INFO}File Information:{C_RESET}")
        print(f"  Size: {C_OK}{self.format_size(file_size)}{C_RESET}")
        print(f"  Type: {C_OK}{file_ext}{C_RESET}\n")
        
        if not self.tool_path:
            Logger.warning("ExifTool not installed - showing basic info only")
            self.basic_file_info(filepath)
            self.show_installation_guide()
            return
        
        # Run exiftool
        try:
            Logger.info("Extracting metadata with ExifTool...")
            
            cmd = ['exiftool', '-j', '-G', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                metadata = json.loads(result.stdout)[0]
                self.display_metadata(metadata, filepath)
                
                # Generate and save report
                report_content = self.generate_report_header("COMPLETE METADATA ANALYSIS", filepath, scan_time)
                report_content += self.format_metadata_for_report(metadata)
                
                self.save_report(report_content, "metadata", filepath)
            else:
                Logger.error("Failed to extract metadata")
                
        except subprocess.TimeoutExpired:
            Logger.error("Analysis timeout!")
        except json.JSONDecodeError:
            Logger.error("Failed to parse metadata")
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
    
    def format_metadata_for_report(self, metadata):
        """Format metadata for txt report"""
        content = ""
        
        # Organize by category
        categories = {}
        for key, value in metadata.items():
            if ':' in key:
                category = key.split(':')[0]
            else:
                category = 'General'
            
            if category not in categories:
                categories[category] = {}
            categories[category][key] = value
        
        # Format organized data
        for category, fields in sorted(categories.items()):
            content += f"\n{'■' * 3} {category.upper()} {'■' * 3}\n"
            content += "-" * 80 + "\n\n"
            
            for key, value in sorted(fields.items()):
                display_key = key.split(':')[-1] if ':' in key else key
                value_str = str(value)
                content += f"{display_key:35} {value_str}\n"
            
            content += "\n"
        
        return content
    
    def analyze_url(self, url):
        """Download and analyze file from URL"""
        clear_screen()
        print_header("URL FILE ANALYSIS", 80)
        
        scan_time = datetime.now()
        print(f"\n{C_OK}[*] Downloading from: {C_WARN}{url}{C_RESET}\n")
        
        try:
            # Download file
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Get filename
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or 'downloaded_file'
            
            # Save temporarily
            temp_file = f"/tmp/{filename}"
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            Logger.success(f"Downloaded: {filename}")
            
            # Analyze with metadata extraction
            if not self.tool_path:
                Logger.warning("ExifTool not installed")
                self.show_installation_guide()
                return
            
            cmd = ['exiftool', '-j', '-G', temp_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                metadata = json.loads(result.stdout)[0]
                self.display_metadata(metadata, temp_file)
                
                # Generate report with URL info
                report_content = self.generate_report_header("URL FILE ANALYSIS", temp_file, scan_time)
                report_content += f"Source URL:     {url}\n"
                report_content += f"Downloaded:     {filename}\n"
                report_content += "=" * 80 + "\n\n"
                report_content += self.format_metadata_for_report(metadata)
                
                self.save_report(report_content, "url_analysis", temp_file)
            
            # Cleanup
            try:
                os.remove(temp_file)
            except:
                pass
                
        except requests.RequestException as e:
            Logger.error(f"Download failed: {str(e)}")
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
    
    def batch_analysis(self, path):
        """Analyze multiple files from directory or single file"""
        clear_screen()
        print_header("BATCH METADATA ANALYSIS", 80)
        
        scan_time = datetime.now()
        files = []
        
        if os.path.isdir(path):
            # Directory - find all supported files
            print(f"\n{C_OK}[*] Scanning directory: {path}{C_RESET}\n")
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    ext = os.path.splitext(filename)[1].lower()
                    if any(ext in formats for formats in self.supported_formats.values()):
                        files.append(filepath)
        elif os.path.isfile(path):
            # Single file provided
            ext = os.path.splitext(path)[1].lower()
            if any(ext in formats for formats in self.supported_formats.values()):
                files.append(path)
                print(f"\n{C_OK}[*] Analyzing single file: {path}{C_RESET}\n")
            else:
                Logger.error(f"Unsupported file format: {ext}")
                return
        else:
            Logger.error("File or directory not found!")
            return
        
        if not files:
            Logger.warning("No supported files found in directory!")
            return
        
        print(f"{C_OK}[*] Found {len(files)} file(s) with metadata to analyze{C_RESET}\n")
        print(f"{C_INFO}Files will be analyzed for:{C_RESET}")
        print(f"  • GPS Coordinates")
        print(f"  • Camera/Device Information")
        print(f"  • Author & Software Details")
        print(f"  • Creation/Modification Dates")
        print(f"  • And all other metadata...\n")
        
        if not self.tool_path:
            Logger.warning("ExifTool not installed!")
            self.show_installation_guide()
            return
        
        results = []
        summary = {
            'total': len(files),
            'success': 0,
            'failed': 0,
            'with_gps': 0,
            'with_author': 0,
        }
        
        for i, filepath in enumerate(files, 1):
            print(f"{C_INFO}[{i}/{len(files)}] Analyzing: {os.path.basename(filepath)}{C_RESET}")
            
            try:
                cmd = ['exiftool', '-j', '-G', filepath]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    metadata = json.loads(result.stdout)[0]
                    
                    # Check for GPS
                    has_gps = any('gps' in k.lower() for k in metadata.keys())
                    if has_gps:
                        summary['with_gps'] += 1
                    
                    # Check for author
                    has_author = any(k in metadata for k in ['Author', 'Creator', 'Artist'])
                    if has_author:
                        summary['with_author'] += 1
                    
                    results.append({
                        'file': filepath,
                        'filename': os.path.basename(filepath),
                        'size': os.path.getsize(filepath),
                        'metadata': metadata,
                        'has_gps': has_gps,
                        'has_author': has_author
                    })
                    
                    summary['success'] += 1
                    print(f"  {C_OK}✓ Success{C_RESET} - {len(metadata)} fields extracted")
                else:
                    summary['failed'] += 1
                    print(f"  {C_ERR}✗ Failed to extract metadata{C_RESET}")
                    
            except Exception as e:
                summary['failed'] += 1
                print(f"  {C_ERR}✗ Error: {str(e)}{C_RESET}")
        
        # Generate batch report
        if results:
            report_content = "=" * 80 + "\n"
            report_content += "BATCH METADATA ANALYSIS REPORT".center(80) + "\n"
            report_content += "=" * 80 + "\n\n"
            report_content += f"Analysis Tool:     ExifTool\n"
            report_content += f"Scan Directory:    {path}\n"
            report_content += f"Scan Date:         {scan_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            report_content += f"Total Files:       {summary['total']}\n"
            report_content += f"Successfully Read: {summary['success']}\n"
            report_content += f"Failed:            {summary['failed']}\n"
            report_content += f"Files with GPS:    {summary['with_gps']}\n"
            report_content += f"Files with Author: {summary['with_author']}\n"
            report_content += "=" * 80 + "\n\n"
            
            # Summary of each file
            report_content += "FILE SUMMARY\n"
            report_content += "-" * 80 + "\n\n"
            
            for idx, item in enumerate(results, 1):
                report_content += f"{idx}. {item['filename']}\n"
                report_content += f"   Path: {item['file']}\n"
                report_content += f"   Size: {self.format_size(item['size'])}\n"
                report_content += f"   Metadata Fields: {len(item['metadata'])}\n"
                report_content += f"   GPS Data: {'Yes' if item['has_gps'] else 'No'}\n"
                report_content += f"   Author Info: {'Yes' if item['has_author'] else 'No'}\n\n"
            
            # Detailed metadata for each file
            report_content += "\n" + "=" * 80 + "\n"
            report_content += "DETAILED METADATA FOR EACH FILE\n"
            report_content += "=" * 80 + "\n\n"
            
            for idx, item in enumerate(results, 1):
                report_content += f"\n{'#' * 80}\n"
                report_content += f"FILE #{idx}: {item['filename']}\n"
                report_content += f"{'#' * 80}\n\n"
                report_content += f"Full Path: {item['file']}\n\n"
                report_content += self.format_metadata_for_report(item['metadata'])
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"batch_analysis_{timestamp}.txt"
            report_path = os.path.join(self.reports_dir, report_filename)
            
            try:
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                
                Logger.success(f"\nBatch report saved: {report_path}")
            except Exception as e:
                Logger.error(f"Failed to save batch report: {str(e)}")
        
        print(f"\n{C_OK}[*] Batch analysis complete!{C_RESET}")
        print(f"\n{C_INFO}Summary:{C_RESET}")
        print(f"  Total Files:       {summary['total']}")
        print(f"  Successful:        {C_OK}{summary['success']}{C_RESET}")
        print(f"  Failed:            {C_ERR if summary['failed'] > 0 else C_OK}{summary['failed']}{C_RESET}")
        print(f"  With GPS Data:     {C_OK}{summary['with_gps']}{C_RESET}")
        print(f"  With Author Info:  {C_OK}{summary['with_author']}{C_RESET}\n")
    
    def convert_gps_to_decimal(self, gps_string):
        """Convert GPS coordinates from DMS to decimal format"""
        try:
            # Example: "41 deg 17' 8.39\" N" -> 41.285664
            import re
            
            # Remove direction letters
            direction = gps_string[-1] if gps_string[-1] in ['N', 'S', 'E', 'W'] else None
            gps_string = gps_string.replace('deg', '').replace("'", '').replace('"', '').strip()
            
            # Extract numbers
            parts = re.findall(r'[\d.]+', gps_string)
            
            if len(parts) >= 3:
                degrees = float(parts[0])
                minutes = float(parts[1])
                seconds = float(parts[2])
                
                # Convert to decimal
                decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
                
                # Apply direction
                if direction in ['S', 'W']:
                    decimal = -decimal
                
                return decimal
            
            # If already in decimal format
            return float(parts[0])
            
        except Exception as e:
            return None
    
    def gps_location_extractor(self, filepath):
        """Extract GPS coordinates"""
        clear_screen()
        print_header("GPS LOCATION EXTRACTION", 80)
        
        scan_time = datetime.now()
        print(f"\n{C_OK}[*] Extracting GPS from: {C_WARN}{filepath}{C_RESET}\n")
        
        if not self.tool_path:
            self.show_installation_guide()
            return
        
        try:
            cmd = ['exiftool', '-j', '-gps*', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)[0]
                
                gps_fields = ['GPSLatitude', 'GPSLongitude', 'GPSAltitude', 
                             'GPSPosition', 'GPSDateTime', 'GPSMapDatum',
                             'GPSLatitudeRef', 'GPSLongitudeRef']
                
                found_gps = False
                gps_data = {}
                
                print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
                print(f"{C_INFO}║  GPS METADATA                                                             ║{C_RESET}")
                print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
                
                for field in gps_fields:
                    if field in data:
                        found_gps = True
                        gps_data[field] = data[field]
                        print(f"{C_OK}{field:20}{C_RESET} {data[field]}")
                
                maps_url = None
                if found_gps:
                    # Generate Google Maps link with decimal coordinates
                    if 'GPSLatitude' in data and 'GPSLongitude' in data:
                        lat_str = data['GPSLatitude']
                        lon_str = data['GPSLongitude']
                        
                        # Convert to decimal
                        lat_decimal = self.convert_gps_to_decimal(lat_str)
                        lon_decimal = self.convert_gps_to_decimal(lon_str)
                        
                        if lat_decimal and lon_decimal:
                            maps_url = f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"
                            
                            print(f"\n{C_INFO}Decimal Coordinates:{C_RESET}")
                            print(f"  Latitude:  {C_OK}{lat_decimal:.6f}{C_RESET}")
                            print(f"  Longitude: {C_OK}{lon_decimal:.6f}{C_RESET}")
                            
                            print(f"\n{C_INFO}Google Maps Link:{C_RESET}")
                            print(f"{C_OK}{maps_url}{C_RESET}")
                            
                            print(f"\n{C_INFO}Alternative Links:{C_RESET}")
                            yandex_url = f"https://yandex.com/maps/?ll={lon_decimal},{lat_decimal}&z=15"
                            osm_url = f"https://www.openstreetmap.org/?mlat={lat_decimal}&mlon={lon_decimal}&zoom=15"
                            print(f"  Yandex Maps: {C_OK}{yandex_url}{C_RESET}")
                            print(f"  OpenStreetMap: {C_OK}{osm_url}{C_RESET}\n")
                        else:
                            print(f"\n{C_WARN}Could not convert coordinates to decimal format{C_RESET}\n")
                    
                    # Generate report
                    report_content = self.generate_report_header("GPS LOCATION EXTRACTION", filepath, scan_time)
                    report_content += "GPS COORDINATES FOUND\n"
                    report_content += "-" * 80 + "\n\n"
                    
                    for field, value in gps_data.items():
                        report_content += f"{field:25} {value}\n"
                    
                    if maps_url:
                        report_content += f"\n\nDECIMAL COORDINATES\n"
                        report_content += "-" * 80 + "\n\n"
                        report_content += f"Latitude:              {lat_decimal:.6f}\n"
                        report_content += f"Longitude:             {lon_decimal:.6f}\n"
                        
                        report_content += f"\n\nMAP LINKS\n"
                        report_content += "-" * 80 + "\n\n"
                        report_content += f"Google Maps:\n{maps_url}\n\n"
                        report_content += f"Yandex Maps:\n{yandex_url}\n\n"
                        report_content += f"OpenStreetMap:\n{osm_url}\n\n"
                        
                        report_content += f"\nLOCATION INFORMATION\n"
                        report_content += "-" * 80 + "\n\n"
                        report_content += f"These coordinates point to a specific location where this image\n"
                        report_content += f"was taken. You can use any of the map links above to view the\n"
                        report_content += f"exact location on a map.\n\n"
                        report_content += f"Altitude: {gps_data.get('GPSAltitude', 'Unknown')}\n"
                        if 'GPSDateTime' in gps_data:
                            report_content += f"GPS Timestamp: {gps_data['GPSDateTime']}\n"
                    
                    self.save_report(report_content, "gps_location", filepath)
                else:
                    Logger.warning("No GPS data found in file")
                    
                    # Still save report showing no GPS
                    report_content = self.generate_report_header("GPS LOCATION EXTRACTION", filepath, scan_time)
                    report_content += "RESULT: No GPS data found in this file\n\n"
                    report_content += "This file does not contain GPS coordinates.\n"
                    report_content += "GPS data is typically found in photos taken with smartphones\n"
                    report_content += "or cameras with GPS enabled.\n"
                    
                    self.save_report(report_content, "gps_location", filepath)
                    
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
    
    def camera_device_info(self, filepath):
        """Extract camera/device information"""
        clear_screen()
        print_header("CAMERA/DEVICE INFORMATION", 80)
        
        scan_time = datetime.now()
        print(f"\n{C_OK}[*] Analyzing device info: {C_WARN}{filepath}{C_RESET}\n")
        
        if not self.tool_path:
            self.show_installation_guide()
            return
        
        try:
            cmd = ['exiftool', '-j', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)[0]
                
                device_fields = {
                    'Camera Info': ['Make', 'Model', 'LensModel', 'SerialNumber'],
                    'Settings': ['ISO', 'ShutterSpeed', 'Aperture', 'FocalLength', 'Flash'],
                    'Software': ['Software', 'ProcessingSoftware', 'CreatorTool'],
                    'Device': ['DeviceManufacturer', 'DeviceModel', 'HostComputer']
                }
                
                report_content = self.generate_report_header("CAMERA/DEVICE INFORMATION", filepath, scan_time)
                found_any = False
                
                for category, fields in device_fields.items():
                    found = False
                    category_data = {}
                    
                    for field in fields:
                        for key in data.keys():
                            if field.lower() in key.lower():
                                category_data[key] = data[key]
                                found = True
                                found_any = True
                    
                    if found:
                        print(f"\n{C_OK}■ {category}{C_RESET}")
                        print(f"{C_INFO}{'─' * 77}{C_RESET}")
                        
                        report_content += f"\n{'■' * 3} {category.upper()} {'■' * 3}\n"
                        report_content += "-" * 80 + "\n\n"
                        
                        for key, value in category_data.items():
                            print(f"  {key:30} {value}")
                            report_content += f"{key:35} {value}\n"
                        
                        report_content += "\n"
                
                if not found_any:
                    msg = "No camera or device information found in this file"
                    Logger.warning(msg)
                    report_content += f"\nRESULT: {msg}\n"
                
                self.save_report(report_content, "camera_device", filepath)
                            
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
    
    def author_software_info(self, filepath):
        """Extract author and software information"""
        clear_screen()
        print_header("AUTHOR & SOFTWARE INFORMATION", 80)
        
        scan_time = datetime.now()
        print(f"\n{C_OK}[*] Extracting creator info: {C_WARN}{filepath}{C_RESET}\n")
        
        if not self.tool_path:
            self.show_installation_guide()
            return
        
        try:
            cmd = ['exiftool', '-j', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)[0]
                
                author_fields = ['Author', 'Creator', 'Artist', 'By-line', 'Writer', 
                               'OwnerName', 'Copyright', 'CopyrightNotice']
                
                software_fields = ['Software', 'CreatorTool', 'ProcessingSoftware', 
                                 'Application', 'Producer', 'HistorySoftwareAgent']
                
                report_content = self.generate_report_header("AUTHOR & SOFTWARE INFORMATION", filepath, scan_time)
                
                # Author info
                print(f"{C_OK}■ Author Information{C_RESET}")
                print(f"{C_INFO}{'─' * 77}{C_RESET}")
                report_content += "\n" + "■" * 3 + " AUTHOR INFORMATION " + "■" * 3 + "\n"
                report_content += "-" * 80 + "\n\n"
                
                found_author = False
                for field in author_fields:
                    if field in data:
                        print(f"  {field:30} {data[field]}")
                        report_content += f"{field:35} {data[field]}\n"
                        found_author = True
                
                if not found_author:
                    msg = "No author information found"
                    print(f"  {C_WARN}{msg}{C_RESET}")
                    report_content += f"{msg}\n"
                
                report_content += "\n"
                
                # Software info
                print(f"\n{C_OK}■ Software Used{C_RESET}")
                print(f"{C_INFO}{'─' * 77}{C_RESET}")
                report_content += "\n" + "■" * 3 + " SOFTWARE USED " + "■" * 3 + "\n"
                report_content += "-" * 80 + "\n\n"
                
                found_software = False
                for field in software_fields:
                    if field in data:
                        print(f"  {field:30} {data[field]}")
                        report_content += f"{field:35} {data[field]}\n"
                        found_software = True
                
                if not found_software:
                    msg = "No software information found"
                    print(f"  {C_WARN}{msg}{C_RESET}")
                    report_content += f"{msg}\n"
                
                self.save_report(report_content, "author_software", filepath)
                    
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
    
    def timeline_analysis(self, filepath):
        """Extract and analyze timestamps"""
        clear_screen()
        print_header("TIMELINE ANALYSIS", 80)
        
        scan_time = datetime.now()
        print(f"\n{C_OK}[*] Analyzing timestamps: {C_WARN}{filepath}{C_RESET}\n")
        
        if not self.tool_path:
            self.show_installation_guide()
            return
        
        try:
            cmd = ['exiftool', '-j', '-time:all', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)[0]
                
                timestamps = {}
                for key, value in data.items():
                    if 'date' in key.lower() or 'time' in key.lower():
                        timestamps[key] = value
                
                report_content = self.generate_report_header("TIMELINE ANALYSIS", filepath, scan_time)
                
                if timestamps:
                    print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
                    print(f"{C_INFO}║  TIMELINE METADATA                                                        ║{C_RESET}")
                    print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
                    
                    report_content += "TIMESTAMP METADATA\n"
                    report_content += "-" * 80 + "\n\n"
                    
                    for key, value in sorted(timestamps.items()):
                        print(f"{C_OK}{key:40}{C_RESET} {value}")
                        report_content += f"{key:45} {value}\n"
                    
                    # Analysis
                    report_content += "\n\nTIMELINE ANALYSIS\n"
                    report_content += "-" * 80 + "\n\n"
                    report_content += f"Total timestamps found: {len(timestamps)}\n"
                    report_content += "\nThese timestamps can reveal:\n"
                    report_content += "  • When the file was originally created\n"
                    report_content += "  • When it was last modified\n"
                    report_content += "  • When the photo was taken (if image)\n"
                    report_content += "  • Software processing dates\n"
                else:
                    Logger.warning("No timestamp metadata found")
                    report_content += "RESULT: No timestamp metadata found\n"
                
                self.save_report(report_content, "timeline", filepath)
                    
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
    
    def remove_metadata(self, filepath):
        """Remove metadata from file"""
        clear_screen()
        print_header("METADATA REMOVAL", 80)
        
        scan_time = datetime.now()
        print(f"\n{C_WARN}[!] This will remove ALL metadata from: {filepath}{C_RESET}\n")
        
        confirm = input(f"{C_INFO}Continue? (yes/no): {C_RESET}").strip().lower()
        
        if confirm != 'yes':
            Logger.info("Operation cancelled")
            return
        
        if not self.tool_path:
            self.show_installation_guide()
            return
        
        try:
            # First, extract current metadata for report
            cmd_extract = ['exiftool', '-j', filepath]
            result_before = subprocess.run(cmd_extract, capture_output=True, text=True)
            metadata_before = json.loads(result_before.stdout)[0] if result_before.returncode == 0 else {}
            
            # Remove metadata
            cmd = ['exiftool', '-all=', '-overwrite_original', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                Logger.success("Metadata removed successfully!")
                
                # Generate removal report
                report_content = "=" * 80 + "\n"
                report_content += "METADATA REMOVAL REPORT".center(80) + "\n"
                report_content += "=" * 80 + "\n\n"
                report_content += f"Tool:           ExifTool\n"
                report_content += f"Target File:    {filepath}\n"
                report_content += f"Date:           {scan_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                report_content += f"Status:         SUCCESS - All metadata removed\n"
                report_content += "=" * 80 + "\n\n"
                
                report_content += "METADATA BEFORE REMOVAL\n"
                report_content += "-" * 80 + "\n\n"
                report_content += f"Total fields removed: {len(metadata_before)}\n\n"
                
                for key, value in sorted(metadata_before.items()):
                    report_content += f"{key:40} {value}\n"
                
                report_content += "\n" + "=" * 80 + "\n"
                report_content += "The file has been cleaned of all metadata.\n"
                report_content += "Original metadata is preserved in this report.\n"
                
                self.save_report(report_content, "metadata_removal", filepath)
            else:
                Logger.error("Failed to remove metadata")
                
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
    
    def show_supported_formats(self):
        """Display supported file formats"""
        clear_screen()
        print_header("SUPPORTED FILE FORMATS", 80)
        
        print(f"\n{C_INFO}ExifTool supports 300+ file formats including:{C_RESET}\n")
        
        for category, extensions in self.supported_formats.items():
            print(f"\n{C_OK}■ {category}{C_RESET}")
            print(f"{C_INFO}{'─' * 77}{C_RESET}")
            print(f"  {', '.join(extensions)}")
        
        print(f"\n{C_INFO}And many more: RAW formats (CR2, NEF, ARW), 3D models,{C_RESET}")
        print(f"{C_INFO}fonts, executables, archives, and specialized formats.{C_RESET}\n")
    
    def display_metadata(self, metadata, filepath):
        """Display extracted metadata in organized format"""
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  EXTRACTED METADATA                                                       ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        # Organize by category
        categories = {}
        for key, value in metadata.items():
            if ':' in key:
                category = key.split(':')[0]
            else:
                category = 'General'
            
            if category not in categories:
                categories[category] = {}
            categories[category][key] = value
        
        # Display organized
        for category, fields in sorted(categories.items()):
            print(f"\n{C_OK}■ {category}{C_RESET}")
            print(f"{C_INFO}{'─' * 77}{C_RESET}")
            for key, value in sorted(fields.items()):
                display_key = key.split(':')[-1] if ':' in key else key
                value_str = str(value)[:60]
                print(f"  {display_key:30} {value_str}")
    
    def basic_file_info(self, filepath):
        """Show basic file info without exiftool"""
        stat = os.stat(filepath)
        
        print(f"{C_INFO}Basic File Information:{C_RESET}")
        print(f"  Created:  {datetime.fromtimestamp(stat.st_ctime)}")
        print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime)}")
        print(f"  Accessed: {datetime.fromtimestamp(stat.st_atime)}")
        print(f"  Size:     {self.format_size(stat.st_size)}\n")
    
    def show_installation_guide(self):
        """Show exiftool installation guide"""
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  EXIFTOOL INSTALLATION                                                    ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}Ubuntu/Debian:{C_RESET}")
        print(f"  sudo apt-get install exiftool\n")
        
        print(f"{C_OK}macOS:{C_RESET}")
        print(f"  brew install exiftool\n")
        
        print(f"{C_OK}Manual:{C_RESET}")
        print(f"  https://exiftool.org/\n")
    
    def format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            if choice == '9':
                self.show_supported_formats()
                pause()
                continue
            
            if choice in ['1', '4', '5', '6', '7', '8']:
                clear_screen()
                print_header("FILE INPUT", 80)
                filepath = input(f"\n{C_INFO}Enter file path: {C_RESET}").strip()
                
                if not filepath:
                    Logger.warning("File path required!")
                    pause()
                    continue
                
                if choice == '1':
                    self.analyze_local_file(filepath)
                elif choice == '4':
                    self.gps_location_extractor(filepath)
                elif choice == '5':
                    self.camera_device_info(filepath)
                elif choice == '6':
                    self.author_software_info(filepath)
                elif choice == '7':
                    self.timeline_analysis(filepath)
                elif choice == '8':
                    self.remove_metadata(filepath)
                
                pause()
                
            elif choice == '2':
                clear_screen()
                print_header("URL INPUT", 80)
                url = input(f"\n{C_INFO}Enter URL: {C_RESET}").strip()
                
                if url:
                    self.analyze_url(url)
                else:
                    Logger.warning("URL required!")
                
                pause()
                
            elif choice == '3':
                clear_screen()
                print_header("BATCH ANALYSIS", 80)
                print(f"\n{C_INFO}You can provide:{C_RESET}")
                print(f"  • Directory path (to scan all files)")
                print(f"  • Single file path (to analyze one file)\n")
                path = input(f"{C_INFO}Enter path: {C_RESET}").strip()
                
                if path:
                    self.batch_analysis(path)
                else:
                    Logger.warning("Path required!")
                
                pause()
                
            else:
                Logger.error("Invalid choice!")
                pause()


def run_exiftool():
    """Entry point"""
    tool = ExifTool()
    tool.run()


if __name__ == "__main__":
    run_exiftool()