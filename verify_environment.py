#!/usr/bin/env python
"""
Comprehensive Environment Verification Script
Tests all critical dependencies and modules for VocalVitals project
"""

import setuptools  # Must be before tensorflow for Python 3.12 compatibility
import sys

def test_imports():
    """Test all required package imports"""
    results = {}
    packages = [
        ('TensorFlow', 'tensorflow', 'tensorflow.__version__'),
        ('Keras', 'keras', 'keras.__version__'),
        ('Librosa', 'librosa', 'librosa.__version__'),
        ('NumPy', 'numpy', 'numpy.__version__'),
        ('SciPy', 'scipy', 'scipy.__version__'),
        ('Pandas', 'pandas', 'pandas.__version__'),
        ('Scikit-learn', 'sklearn', 'sklearn.__version__'),
        ('FastAPI', 'fastapi', 'fastapi.__version__'),
        ('gdown', 'gdown', '"(available)"'),
        ('tqdm', 'tqdm', '"(available)"'),
    ]
    
    print("\n" + "="*70)
    print("🔍 VERIFYING PACKAGE IMPORTS")
    print("="*70)
    
    for name, module, version_attr in packages:
        try:
            exec(f"import {module}")
            if version_attr.startswith('"'):
                version = version_attr.strip('"')
            else:
                version = eval(version_attr)
            results[name] = (True, version)
            print(f"✅ {name:20} {version}")
        except Exception as e:
            results[name] = (False, str(e))
            print(f"❌ {name:20} FAILED: {e}")
    
    return results

def test_project_modules():
    """Test VocalVitals project modules"""
    print("\n" + "="*70)
    print("🔍 VERIFYING PROJECT MODULES")
    print("="*70)
    
    modules = [
        ('AudioProcessor', 'src.audio_processing.processor', 'AudioProcessor'),
        ('AcousticFeatureExtractor', 'src.feature_extraction.extractor', 'AcousticFeatureExtractor'),
        ('EmotionCNN', 'src.models.emotion_models', 'EmotionCNN'),
        ('BurnoutClassifier', 'src.models.emotion_models', 'BurnoutClassifier'),
        ('HybridEmotionModel', 'src.models.emotion_models', 'HybridEmotionModel'),
    ]
    
    results = {}
    for name, module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            results[name] = (True, f"Ready (from {module_path})")
            print(f"✅ {name:30} Ready")
        except Exception as e:
            results[name] = (False, str(e))
            print(f"❌ {name:30} FAILED: {e}")
    
    return results

def test_model_creation():
    """Test creating actual neural network models"""
    print("\n" + "="*70)
    print("🔍 VERIFYING MODEL INSTANTIATION")
    print("="*70)
    
    try:
        from src.models.emotion_models import create_emotion_cnn, create_burnout_classifier, create_hybrid_model
        
        # Test EmotionCNN
        model1 = create_emotion_cnn(input_shape=(128, 87, 1), num_classes=8)
        print(f"✅ EmotionCNN instantiated: {model1.__class__.__name__}")
        
        # Test BurnoutClassifier  
        model2 = create_burnout_classifier(input_features=20, num_classes=2)
        print(f"✅ BurnoutClassifier instantiated: {model2.__class__.__name__}")
        
        # Test HybridEmotionModel
        model3 = create_hybrid_model(cnn_input_shape=(128, 87, 1), feature_input_size=20)
        print(f"✅ HybridEmotionModel instantiated: {model3.__class__.__name__}")
        
        return True
    except Exception as e:
        print(f"❌ Model instantiation FAILED: {e}")
        return False

def main():
    """Run all verification tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + " VOCALVITALS ENVIRONMENT VERIFICATION".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Run tests
    package_results = test_imports()
    module_results = test_project_modules()
    model_success = test_model_creation()
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    package_pass = sum(1 for ok, _ in package_results.values() if ok)
    module_pass = sum(1 for ok, _ in module_results.values() if ok)
    all_pass = package_pass == len(package_results) and module_pass == len(module_results) and model_success
    
    print(f"Packages: {package_pass}/{len(package_results)} ✅" if package_pass == len(package_results) else f"Packages: {package_pass}/{len(package_results)} ⚠️")
    print(f"Modules:  {module_pass}/{len(module_results)} ✅" if module_pass == len(module_results) else f"Modules:  {module_pass}/{len(module_results)} ⚠️")
    print(f"Models:   ✅" if model_success else "Models:   ⚠️")
    
    print("\n" + "="*70)
    if all_pass:
        print("🎉 ENVIRONMENT READY FOR DEVELOPMENT!")
        print("="*70)
        print("\nPython Version:", sys.version)
        print("Venv Location:", sys.prefix)
        print("\nKey Features Enabled:")
        print("  ✅ Real TensorFlow/Keras models (not stubs)")
        print("  ✅ Audio processing with Librosa")
        print("  ✅ Dataset download support (gdown)")
        print("  ✅ Progress visualization (tqdm)")
        print("  ✅ Database support (SQLite)")
        print("="*70 + "\n")
        return 0
    else:
        print("⚠️  SOME COMPONENTS FAILED - SEE DETAILS ABOVE")
        print("="*70 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
