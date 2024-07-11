import unreal
import os

def count_packages_and_find_top10(output_file):
    # Get the asset registry
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    # Get all assets
    all_assets = asset_registry.get_all_assets()

    # Dictionary to store the count of packages per directory and file
    package_count_per_directory = {}
    package_count_per_file = {}

    # Iterate through all assets and count packages
    for asset in all_assets:
        asset_path = str(asset.package_name)  # Ensure asset_path is a string
        asset_name = str(asset.asset_name)    # Ensure asset_name is a string
        asset_dir = "/".join(asset_path.split("/")[:-1])  # Get directory path

        # Update directory package count
        if asset_dir in package_count_per_directory:
            package_count_per_directory[asset_dir] += 1
        else:
            package_count_per_directory[asset_dir] = 1

        # Update file package count
        if asset_name in package_count_per_file:
            package_count_per_file[asset_name] += 1
        else:
            package_count_per_file[asset_name] = 1

    # Sort directories and files by package count and get top 10
    top10_dirs = sorted(package_count_per_directory.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_files = sorted(package_count_per_file.items(), key=lambda x: x[1], reverse=True)[:10]

    # Prepare the results
    results = ["Top 10 Directories with the most packages:"]
    for dir, count in top10_dirs:
        results.append(f"{dir}: {count} packages")
    
    results.append("\nTop 10 Files with the most packages:")
    for file, count in top10_files:
        results.append(f"{file}: {count} packages")

    # Save the results to a file
    with open(output_file, 'w') as file:
        for line in results:
            file.write(line + '\n')

    # Print the results to the Output Log as well
    for line in results:
        unreal.log(line)

# Define the output file path
output_file = os.path.join(unreal.Paths.project_saved_dir(), 'package_report.txt')

# Call the function
count_packages_and_find_top10(output_file)