import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Read the NetCDF file using xarray
ds = xr.open_dataset('GRIDMET PRECIP DATA')

# Set the time range for the analysis
start_date = '1990-12-01'
end_date = '2020-12-31'

# Slice the dataset to the desired time period
ds_subset = ds.sel(day=slice(start_date, end_date))

# Calculate the annual climatology
climatology = ds_subset['precipitation_amount'].groupby('day.year').sum(dim='day')

# Calculate the climatology as the mean of the total annual precipitation over the 30-year period
climatology = climatology.mean(dim='year')

# Mask out values below or equal to 0
masked_climatology = np.ma.masked_where(climatology <= 0, climatology)


# Plot the annual climatology
projection = ccrs.PlateCarree()
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6), subplot_kw={'projection': projection})

ax.set_title('Gridmet Annual Precipitation Climatology (1979-2020)')
ax.set_extent([ds.lon.min(), ds.lon.max(), ds.lat.min(), ds.lat.max()], crs=projection)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.5)
ax.add_feature(cfeature.STATES, linewidth=0.5)
ax.add_feature(cfeature.OCEAN, facecolor='dodgerblue')
im = ax.pcolormesh(ds.lon, ds.lat, masked_climatology, cmap='BrBG', vmin=0, vmax=2000, transform=projection)
ax.annotate('Data Source: Gridmet', xy=(0.05, 0.08), xycoords='axes fraction', fontsize=8, bbox=dict(facecolor='white', edgecolor='black', alpha=0.7, boxstyle='round,pad=0.5'))

plt.colorbar(im, ax=ax, orientation='horizontal', label='Precipitation (mm)', pad=0.03)

fig.subplots_adjust(wspace=0.1, hspace=0.3)
plt.savefig('annual_climatology_precip_1991_2020.png', dpi=300, bbox_inches='tight')
plt.show()

